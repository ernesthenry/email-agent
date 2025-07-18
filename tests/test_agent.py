import pytest
from datetime import datetime
from src.agent import EmailAgent
from src.models import EmailData

@pytest.fixture
def agent():
    return EmailAgent()

@pytest.fixture
def test_email():
    return EmailData(
        sender="test@example.com",
        subject="Test Subject",
        content="Test content",
        received_at=datetime.now()
    )

def test_agent_initialization(agent):
    assert agent.llm is not None
    assert agent.graph is not None

def test_email_processing(agent, test_email):
    result = agent.process_email(test_email)
    assert result is not None
    assert "email" in result
    assert "classification" in result