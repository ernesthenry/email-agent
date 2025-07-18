import os
from datetime import datetime
from dotenv import load_dotenv
from .agent import EmailAgent
from .models import EmailData

def load_environment():
    """Load environment variables"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

def create_test_emails():
    """Create test emails for demonstration"""
    return [
        EmailData(
            sender="ceo@company.com",
            sender_title="CEO",
            sender_company="Important Corp",
            subject="Meeting Request: Q4 Strategy Discussion",
            content="Hi, I'd like to schedule a meeting next week to discuss our Q4 strategy. Are you available Tuesday or Wednesday afternoon?",
            received_at=datetime.now()
        ),
        EmailData(
            sender="support@customer.com",
            subject="Question about your product features",
            content="Hello, I'm interested in learning more about your product's API capabilities. Can you provide some documentation?",
            received_at=datetime.now()
        ),
        EmailData(
            sender="newsletter@spam.com",
            subject="🎉 Amazing deals just for you!",
            content="Don't miss out on these incredible deals! Click here to save 90% on everything!",
            received_at=datetime.now()
        )
    ]

def main():
    """Main application entry point"""
    try:
        # Load environment
        load_environment()
        
        # Initialize agent
        agent = EmailAgent()
        
        # Get test emails
        test_emails = create_test_emails()
        
        # Process each email
        for i, email in enumerate(test_emails, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING EMAIL {i}")
            print(f"{'='*60}")
            print(f"From: {email.sender}")
            print(f"Subject: {email.subject}")
            print(f"Content: {email.content[:100]}...")
            
            try:
                result = agent.process_email(email)
                
                if result.get("error"):
                    print(f"❌ Error: {result['error']}")
                else:
                    classification = result.get("classification")
                    if classification:
                        print(f"✅ Classification: {classification.intent.value} ({classification.urgency.value})")
                        print(f"📝 Reasoning: {classification.reasoning}")
                        
                        if classification.requires_response:
                            print(f"📧 Response drafted and {'sent' if result.get('should_send') else 'pending approval'}")
                        else:
                            print(f"🚫 No response needed")
                    
            except Exception as e:
                print(f"❌ Processing failed: {str(e)}")
                
    except Exception as e:
        print(f"❌ Application failed to start: {str(e)}")

if __name__ == "__main__":
    main()
