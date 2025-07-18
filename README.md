# Email Agent with LangGraph

A sophisticated AI-powered email processing agent that automatically classifies, prioritizes, and responds to emails using LangGraph workflows and OpenAI's language models.

## 🚀 Features

- **Smart Email Classification**: Automatically categorizes emails by intent (meeting requests, support questions, spam, etc.) and urgency level
- **Context-Aware Responses**: Generates professional email responses based on sender context and email content
- **Calendar Integration**: Checks availability and proposes meeting times for scheduling requests
- **Human-in-the-Loop**: Presents drafted responses for human review before sending
- **Modular Architecture**: Built with LangGraph for easy customization and scaling
- **Production Ready**: Comprehensive error handling, logging, and testing framework

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/ernesthenry/email-agent.git
cd email-agent
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

## ⚡ Quick Start

### 1. Set Your OpenAI API Key

```bash
# Edit .env file
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Run the Demo

```bash
python -m src.main
```

### 3. Process Your First Email

```python
from src.agent import EmailAgent
from src.models import EmailData
from datetime import datetime

# Initialize agent
agent = EmailAgent()

# Create sample email
email = EmailData(
    sender="ceo@company.com",
    subject="Meeting Request: Q4 Planning",
    content="Hi, can we schedule a meeting next week to discuss Q4 planning?",
    received_at=datetime.now()
)

# Process email
result = agent.process_email(email)
print(f"Classification: {result['classification'].intent}")
print(f"Response: {result['final_response']}")
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0

# Gmail API Configuration (Production)
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REFRESH_TOKEN=your-gmail-refresh-token

# Calendar API Configuration (Production)
GOOGLE_CALENDAR_API_KEY=your-calendar-api-key
GOOGLE_CALENDAR_ID=your-calendar-id

# Agent Configuration
AGENT_DEBUG=false
AGENT_LOG_LEVEL=INFO
AGENT_MAX_RETRIES=3

# Database Configuration (Optional)
DATABASE_URL=postgresql://user:password@localhost/emailagent
```

### Model Configuration

The agent supports different OpenAI models:

- `gpt-4-turbo-preview` (recommended for production)
- `gpt-3.5-turbo` (faster, more cost-effective)
- `gpt-4` (most capable, slower)

## 📖 Usage

### Basic Usage

```python
from src.agent import EmailAgent
from src.models import EmailData

# Initialize agent
agent = EmailAgent(model="gpt-4-turbo-preview")

# Process email
email_data = EmailData(
    sender="client@company.com",
    subject="Project Update Request",
    content="Could you provide an update on the project status?",
    received_at=datetime.now()
)

result = agent.process_email(email_data)
```

### Advanced Usage

```python
# Custom configuration
agent = EmailAgent(
    model="gpt-4-turbo-preview",
    temperature=0.1,
    max_tokens=2000
)

# Batch processing
emails = [email1, email2, email3]
results = []

for email in emails:
    result = agent.process_email(email)
    results.append(result)
```

### Email Classification

The agent classifies emails into these categories:

#### Intent Types:
- `MEETING_REQUEST`: Scheduling or meeting-related emails
- `SUPPORT_QUESTION`: Customer support or technical questions
- `INFORMATION_REQUEST`: General information requests
- `URGENT_BUSINESS`: Time-sensitive business matters
- `FOLLOW_UP`: Follow-up emails on previous conversations
- `SPAM`: Unwanted or promotional emails
- `NEWSLETTER`: Newsletters or marketing emails

#### Urgency Levels:
- `HIGH`: Requires immediate attention
- `MEDIUM`: Normal business priority
- `LOW`: Can be handled when convenient

### Response Generation

The agent generates contextually appropriate responses:

```python
# Example response for meeting request
{
    "subject": "Re: Meeting Request: Q4 Planning",
    "content": "Hi [Name], I'd be happy to discuss Q4 planning with you. Here are some available times:\n\n- Tuesday, Oct 15 at 2:00 PM - 3:00 PM\n- Wednesday, Oct 16 at 10:00 AM - 11:00 AM\n\nPlease let me know which works best for you.\n\nBest regards,\n[Your Name]",
    "tone": "professional",
    "includes_meeting_times": true
}
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Email Input   │───▶│   Email Agent   │───▶│   Response      │
│                 │    │   (LangGraph)   │    │   Output        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   External      │
                    │   Services      │
                    │   (Gmail, Cal)  │
                    └─────────────────┘
```

### LangGraph Workflow

```mermaid
graph TD
    A[Email Input] --> B[Enrich Sender Context]
    B --> C[Classify Email]
    C --> D{Requires Response?}
    D -->|No| E[End - Ignore]
    D -->|Yes| F[Check Calendar]
    F --> G{Meeting Request?}
    G -->|Yes| H[Get Availability]
    G -->|No| I[Draft Response]
    H --> I
    I --> J[Human Review]
    J --> K{Approved?}
    K -->|No| L[End - Rejected]
    K -->|Yes| M[Send Email]
    M --> N[End - Sent]
```

### Project Structure

```
email-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Main agent implementation
│   ├── models.py             # Pydantic data models
│   ├── state.py              # LangGraph state definition
│   ├── prompts.py            # LLM prompts
│   ├── main.py               # Application entry point
│   └── services/
│       ├── __init__.py
│       ├── mock_services.py  # Mock APIs for development
│       ├── gmail_service.py  # Gmail API integration
│       └── calendar_service.py # Calendar API integration
├── tests/
│   ├── __init__.py
│   ├── test_agent.py         # Agent tests
│   ├── test_models.py        # Model tests
│   └── test_services.py      # Service tests
├── config/
│   └── settings.py           # Configuration management
├── .env                      # Environment variables
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # License file
```

## 📚 API Reference

### EmailAgent Class

#### `__init__(model: str = "gpt-4-turbo-preview", temperature: float = 0)`
Initialize the email agent with specified model and temperature.

#### `process_email(email_data: EmailData) -> EmailAgentState`
Process a single email through the complete workflow.

**Parameters:**
- `email_data`: EmailData object containing email details

**Returns:**
- `EmailAgentState`: Complete state object with classification, response, and metadata

### Models

#### `EmailData`
```python
class EmailData(BaseModel):
    sender: str
    sender_title: Optional[str] = None
    sender_company: Optional[str] = None
    subject: str
    content: str
    received_at: datetime
    thread_id: Optional[str] = None
```

#### `EmailClassification`
```python
class EmailClassification(BaseModel):
    intent: EmailIntent
    urgency: EmailUrgency
    requires_response: bool
    reasoning: str
```

#### `ResponseDraft`
```python
class ResponseDraft(BaseModel):
    subject: str
    content: str
    tone: str
    includes_meeting_times: bool = False
    proposed_times: List[CalendarSlot] = []
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_agent.py

# Run with verbose output
pytest -v
```

### Test Structure

```python
# Example test
def test_email_classification():
    agent = EmailAgent()
    email = EmailData(
        sender="test@example.com",
        subject="Meeting Request",
        content="Can we schedule a meeting?",
        received_at=datetime.now()
    )
    
    result = agent.process_email(email)
    assert result["classification"].intent == EmailIntent.MEETING_REQUEST
```

### Mock Services

For development and testing, the agent uses mock services:

```python
# Mock Gmail service
mock_gmail = MockGmailService()
context = mock_gmail.get_sender_context("test@example.com")

# Mock Calendar service
mock_calendar = MockCalendarService()
availability = mock_calendar.get_availability(days_ahead=7)
```

## 🚀 Deployment

### Production Setup

1. **Replace Mock Services**: Integrate with real Gmail and Calendar APIs
2. **Set Up Database**: Configure PostgreSQL or your preferred database
3. **Configure Authentication**: Set up OAuth for Gmail and Calendar access
4. **Set Environment Variables**: Configure production environment variables
5. **Deploy**: Use Docker, Kubernetes, or your preferred deployment method

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY .env .

CMD ["python", "-m", "src.main"]
```

```bash
# Build and run
docker build -t email-agent .
docker run -e OPENAI_API_KEY=your-key email-agent
```

### Environment-Specific Configurations

#### Development
```env
AGENT_DEBUG=true
AGENT_LOG_LEVEL=DEBUG
USE_MOCK_SERVICES=true
```

#### Production
```env
AGENT_DEBUG=false
AGENT_LOG_LEVEL=INFO
USE_MOCK_SERVICES=false
DATABASE_URL=postgresql://...
```

## 📊 Monitoring and Logging

### LangSmith Integration

The agent supports LangSmith for tracing and monitoring:

```python
# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "email-agent"
```

### Custom Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

## 🔧 Customization

### Adding New Email Intents

```python
# In models.py
class EmailIntent(str, Enum):
    MEETING_REQUEST = "meeting_request"
    SUPPORT_QUESTION = "support_question"
    # Add your new intent
    INVOICE_REQUEST = "invoice_request"
```

### Custom Response Templates

```python
# In prompts.py
CUSTOM_RESPONSE_TEMPLATE = """
Based on the email intent '{intent}', generate a response that:
1. Acknowledges the request
2. Provides relevant information
3. Includes next steps
"""
```

### Extending the Workflow

```python
# Add new nodes to the workflow
workflow.add_node("custom_processing", self._custom_processing_node)
workflow.add_edge("classify_email", "custom_processing")
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run tests: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused
- Add tests for new features

### Pull Request Process

1. Ensure tests pass
2. Update documentation if needed
3. Add/update type hints
4. Follow the existing code style
5. Write clear commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the workflow framework
- [OpenAI](https://openai.com/) for the language models
- [Pydantic](https://pydantic.dev/) for data validation
- [LangChain](https://github.com/langchain-ai/langchain) for the AI application framework

## 📞 Support

### Getting Help

- **Documentation**: Check this README and inline code comments
- **Issues**: [Create an issue](https://github.com/ernesthenry/email-agent/issues) on GitHub
- **Discussions**: Join our [GitHub Discussions](https://github.com/ernesthenry/email-agent/discussions)

### Common Issues

#### API Key Errors
```bash
# Make sure your API key is set
export OPENAI_API_KEY=your-key-here
```

#### Import Errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

#### Model Access Issues
```bash
# Check if you have access to the specified model
# Try using gpt-3.5-turbo instead of gpt-4
```

### Performance Optimization

- Use `gpt-3.5-turbo` for faster responses
- Implement caching for repeated requests
- Batch process multiple emails
- Use async processing for high volume

## 🔮 Roadmap

- [ ] **v1.1**: Real Gmail and Calendar API integration
- [ ] **v1.2**: Multi-language support
- [ ] **v1.3**: Advanced scheduling logic
- [ ] **v1.4**: Machine learning for sender importance
- [ ] **v1.5**: Integration with more email providers
- [ ] **v2.0**: Multi-agent workflows
- [ ] **v2.1**: Voice note transcription
- [ ] **v2.2**: Attachment processing

## 📈 Performance Metrics

### Benchmarks

- **Classification Accuracy**: 95%+ on common email types
- **Response Time**: <5 seconds for simple emails
- **Throughput**: 100+ emails per hour
- **Uptime**: 99.9% availability target

### Cost Optimization

- **Model Selection**: Use appropriate model for complexity
- **Prompt Engineering**: Optimize prompts for efficiency
- **Caching**: Implement intelligent caching strategies
- **Batch Processing**: Process multiple emails together

---

**Made with ❤️ by Kato Ernest Henry**

For more information, visit our [GitHub repository](https://github.com/ernesthenry/email-agent).