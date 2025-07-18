from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class EmailUrgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class EmailIntent(str, Enum):
    MEETING_REQUEST = "meeting_request"
    SUPPORT_QUESTION = "support_question"
    INFORMATION_REQUEST = "information_request"
    SPAM = "spam"
    NEWSLETTER = "newsletter"
    URGENT_BUSINESS = "urgent_business"
    FOLLOW_UP = "follow_up"

class EmailClassification(BaseModel):
    intent: EmailIntent
    urgency: EmailUrgency
    requires_response: bool
    reasoning: str

class EmailData(BaseModel):
    sender: str
    sender_title: Optional[str] = None
    sender_company: Optional[str] = None
    subject: str
    content: str
    received_at: datetime
    thread_id: Optional[str] = None

class CalendarSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    duration_minutes: int

class ResponseDraft(BaseModel):
    subject: str
    content: str
    tone: str
    includes_meeting_times: bool = False
    proposed_times: List[CalendarSlot] = []