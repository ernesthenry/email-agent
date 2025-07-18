from typing import List, Dict
from datetime import datetime, timedelta
from ..models import CalendarSlot

class MockGmailService:
    """Mock Gmail service for development"""
    
    def __init__(self):
        self.mock_contacts = {
            "ceo@company.com": {
                "name": "CEO",
                "title": "Chief Executive Officer",
                "company": "Important Corp",
                "importance": "high",
                "relationship": "key_stakeholder"
            },
            "support@customer.com": {
                "name": "Support Team",
                "title": "Customer Support",
                "company": "Customer Corp",
                "importance": "medium",
                "relationship": "customer"
            }
        }
    
    def get_sender_context(self, email_address: str) -> Dict:
        return self.mock_contacts.get(email_address, {
            "name": email_address,
            "importance": "medium",
            "relationship": "unknown"
        })

class MockCalendarService:
    """Mock Calendar service for development"""
    
    def get_availability(self, days_ahead: int = 7) -> List[CalendarSlot]:
        now = datetime.now()
        slots = []
        
        for day in range(1, days_ahead + 1):
            date = now + timedelta(days=day)
            slots.extend([
                CalendarSlot(
                    start_time=date.replace(hour=9, minute=0, second=0, microsecond=0),
                    end_time=date.replace(hour=10, minute=0, second=0, microsecond=0),
                    duration_minutes=60
                ),
                CalendarSlot(
                    start_time=date.replace(hour=14, minute=0, second=0, microsecond=0),
                    end_time=date.replace(hour=15, minute=0, second=0, microsecond=0),
                    duration_minutes=60
                )
            ])
        
        return slots[:5]