from langchain_core.prompts import ChatPromptTemplate

CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert email classifier. Analyze the email content, sender information, and context to determine:
    1. The primary intent of the email
    2. The urgency level  
    3. Whether it requires a response
    
    Consider sender importance and relationship when determining urgency.
    
    {format_instructions}"""),
    ("human", """
    EMAIL DETAILS:
    From: {sender} ({sender_title} at {sender_company})
    Subject: {subject}
    Content: {content}
    
    SENDER CONTEXT:
    Importance: {importance}
    Relationship: {relationship}
    
    Classify this email:
    """)
])

RESPONSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a professional email response assistant. Draft a response based on the email content, classification, and available context.
    
    GUIDELINES:
    - Match the tone appropriately (formal for business, casual for internal)
    - If meeting request, include available time slots
    - Be concise but complete
    - Include proper salutation and closing
    - For high urgency items, acknowledge the urgency
    
    {format_instructions}"""),
    ("human", """
    ORIGINAL EMAIL:
    From: {sender}
    Subject: {subject}
    Content: {content}
    
    CLASSIFICATION:
    Intent: {intent}
    Urgency: {urgency}
    
    SENDER CONTEXT:
    Importance: {importance}
    Relationship: {relationship}
    
    AVAILABLE TIME SLOTS:
    {availability}
    
    Draft a professional response:
    """)
])
