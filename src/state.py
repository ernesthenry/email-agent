from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from .models import EmailData, EmailClassification, CalendarSlot, ResponseDraft

class EmailAgentState(TypedDict):
    """State for the email agent workflow"""
    email: EmailData
    sender_context: Optional[dict]
    classification: Optional[EmailClassification]
    calendar_availability: Optional[List[CalendarSlot]]
    response_draft: Optional[ResponseDraft]
    final_response: Optional[str]
    should_send: bool
    messages: Annotated[List[BaseMessage], add_messages]
    error: Optional[str]