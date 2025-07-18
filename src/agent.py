import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from .models import EmailData, EmailClassification, ResponseDraft, EmailIntent
from .state import EmailAgentState
from .prompts import CLASSIFICATION_PROMPT, RESPONSE_PROMPT
from .services.mock_services import MockGmailService, MockCalendarService

class EmailAgent:
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.gmail_service = MockGmailService()
        self.calendar_service = MockCalendarService()
        
        # Initialize parsers
        self.classification_parser = PydanticOutputParser(pydantic_object=EmailClassification)
        self.response_parser = PydanticOutputParser(pydantic_object=ResponseDraft)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(EmailAgentState)
        
        # Add nodes
        workflow.add_node("enrich_sender", self._enrich_sender_context)
        workflow.add_node("classify_email", self._classify_email)
        workflow.add_node("check_calendar", self._check_calendar_availability)
        workflow.add_node("draft_response", self._draft_response)
        workflow.add_node("human_review", self._human_review)
        workflow.add_node("send_email", self._send_email)
        
        # Define the flow
        workflow.set_entry_point("enrich_sender")
        workflow.add_edge("enrich_sender", "classify_email")
        workflow.add_conditional_edges(
            "classify_email",
            self._should_respond,
            {
                "respond": "check_calendar",
                "ignore": END
            }
        )
        workflow.add_conditional_edges(
            "check_calendar",
            self._needs_calendar,
            {
                "calendar_needed": "draft_response",
                "no_calendar": "draft_response"
            }
        )
        workflow.add_edge("draft_response", "human_review")
        workflow.add_conditional_edges(
            "human_review",
            self._human_approval,
            {
                "approved": "send_email",
                "rejected": END
            }
        )
        workflow.add_edge("send_email", END)
        
        return workflow.compile()
    
    def _enrich_sender_context(self, state: EmailAgentState) -> EmailAgentState:
        """Enrich sender information from CRM/contacts"""
        email = state["email"]
        sender_context = self.gmail_service.get_sender_context(email.sender)
        
        state["sender_context"] = sender_context
        state["messages"].append(
            HumanMessage(content=f"Enriched sender context for {email.sender}")
        )
        
        return state
    
    def _classify_email(self, state: EmailAgentState) -> EmailAgentState:
        """Classify email intent and urgency"""
        email = state["email"]
        sender_context = state["sender_context"]
        
        formatted_prompt = CLASSIFICATION_PROMPT.format_messages(
            format_instructions=self.classification_parser.get_format_instructions(),
            sender=email.sender,
            sender_title=sender_context.get("title", "Unknown"),
            sender_company=sender_context.get("company", "Unknown"),
            subject=email.subject,
            content=email.content,
            importance=sender_context.get("importance", "medium"),
            relationship=sender_context.get("relationship", "unknown")
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            classification = self.classification_parser.parse(response.content)
            
            state["classification"] = classification
            state["messages"].append(
                AIMessage(content=f"Classified email: {classification.intent.value}, {classification.urgency.value}")
            )
            
        except Exception as e:
            state["error"] = f"Classification failed: {str(e)}"
            state["classification"] = EmailClassification(
                intent=EmailIntent.INFORMATION_REQUEST,
                urgency="medium",
                requires_response=True,
                reasoning="Failed to classify, using default"
            )
        
        return state
    
    def _check_calendar_availability(self, state: EmailAgentState) -> EmailAgentState:
        """Check calendar availability if needed"""
        classification = state["classification"]
        
        if classification.intent == EmailIntent.MEETING_REQUEST:
            availability = self.calendar_service.get_availability()
            state["calendar_availability"] = availability
            
            state["messages"].append(
                HumanMessage(content=f"Retrieved {len(availability)} available time slots")
            )
        
        return state
    
    def _draft_response(self, state: EmailAgentState) -> EmailAgentState:
        """Draft email response"""
        email = state["email"]
        classification = state["classification"]
        sender_context = state["sender_context"]
        calendar_availability = state.get("calendar_availability", [])
        
        # Format availability for prompt
        availability_text = ""
        if calendar_availability:
            availability_text = "\n".join([
                f"- {slot.start_time.strftime('%A, %B %d at %I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
                for slot in calendar_availability
            ])
        else:
            availability_text = "No calendar check needed"
        
        formatted_prompt = RESPONSE_PROMPT.format_messages(
            format_instructions=self.response_parser.get_format_instructions(),
            sender=email.sender,
            subject=email.subject,
            content=email.content,
            intent=classification.intent.value,
            urgency=classification.urgency.value,
            importance=sender_context.get("importance", "medium"),
            relationship=sender_context.get("relationship", "unknown"),
            availability=availability_text
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            draft = self.response_parser.parse(response.content)
            
            state["response_draft"] = draft
            state["messages"].append(
                AIMessage(content=f"Drafted response with tone: {draft.tone}")
            )
            
        except Exception as e:
            state["error"] = f"Response drafting failed: {str(e)}"
            state["response_draft"] = ResponseDraft(
                subject=f"Re: {email.subject}",
                content="Thank you for your email. I'll review this and get back to you soon.",
                tone="professional"
            )
        
        return state
    
    def _human_review(self, state: EmailAgentState) -> EmailAgentState:
        """Present draft for human review"""
        draft = state["response_draft"]
        
        print("\n" + "="*50)
        print("DRAFT EMAIL FOR REVIEW")
        print("="*50)
        print(f"Subject: {draft.subject}")
        print(f"Tone: {draft.tone}")
        print("\nContent:")
        print(draft.content)
        print("\n" + "="*50)
        
        # Auto-approve for demo (replace with real approval logic)
        state["should_send"] = True
        state["final_response"] = draft.content
        
        state["messages"].append(
            HumanMessage(content="Email draft presented for human review")
        )
        
        return state
    
    def _send_email(self, state: EmailAgentState) -> EmailAgentState:
        """Send the approved email"""
        print("\n📧 EMAIL SENT!")
        print(f"Final response: {state['final_response']}")
        
        state["messages"].append(
            AIMessage(content="Email sent successfully")
        )
        
        return state
    
    # Conditional edge functions
    def _should_respond(self, state: EmailAgentState) -> str:
        """Determine if email should receive a response"""
        classification = state["classification"]
        
        if not classification.requires_response:
            return "ignore"
        
        if classification.intent in [EmailIntent.SPAM, EmailIntent.NEWSLETTER]:
            return "ignore"
        
        return "respond"
    
    def _needs_calendar(self, state: EmailAgentState) -> str:
        """Determine if calendar check is needed"""
        classification = state["classification"]
        
        if classification.intent == EmailIntent.MEETING_REQUEST:
            return "calendar_needed"
        
        return "no_calendar"
    
    def _human_approval(self, state: EmailAgentState) -> str:
        """Check if human approved the response"""
        return "approved" if state["should_send"] else "rejected"
    
    def process_email(self, email_data: EmailData) -> EmailAgentState:
        """Process an email through the agent workflow"""
        initial_state = EmailAgentState(
            email=email_data,
            sender_context=None,
            classification=None,
            calendar_availability=None,
            response_draft=None,
            final_response=None,
            should_send=False,
            messages=[],
            error=None
        )
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        return final_state
