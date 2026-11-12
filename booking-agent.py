from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
load_dotenv()

model_name = "gpt-4o-mini"
llm = ChatOpenAI(model=model_name)

SYSTEM_PROMPT = """You are a booking agent for a counselling service. The client details below are already known. 
Use them when you call tools. Do not ask the client for their name, email, or counsellor, and do not ask for a phone number.

Client:
- First name: Jane
- Last name: Smith
- Email: jane.smith@example.com
- Counsellor: Dr. John Doe

Ask only for a date and time when the client has not given them.
When the client gives a date and time, call check_availability before you reply.
if the time and date are not available, ask the client to try again.
if the time and date are available, ask the client if they would like to book the appointment.
"""

@tool
def book_appointment(first_name: str, last_name: str, user_email: str, counsellor_name: str, date: str, time: str):
    """Book an appointment for a client with a counsellor at a date and time."""
    message = f"Booking appointment for {first_name} {last_name} ({user_email}) with {counsellor_name} on {date} at {time}"
    print(message)
    return message

@tool
def check_availability(first_name: str, last_name: str, user_email: str, counsellor_name: str, date: str, time: str):
    """Check whether a counsellor is free for a client at a date and time."""
    message = f"Checking availability for {first_name} {last_name} ({user_email}) with {counsellor_name} on {date} at {time}"
    print(message)
    return "The counsellor is free at the given date and time."

@tool
def cancel_appointment(first_name: str, last_name: str, user_email: str, counsellor_name: str, date: str, time: str):
    """Cancel an existing appointment for a client with a counsellor."""
    message = f"Cancelling appointment for {first_name} {last_name} ({user_email}) with {counsellor_name} on {date} at {time}"
    print(message)
    return message

@tool
def confirm_appointment(first_name: str, last_name: str, user_email: str, counsellor_name: str, date: str, time: str):
    """Confirm an appointment for a client with a counsellor at a date and time."""
    message = f"Confirming appointment for {first_name} {last_name} ({user_email}) with {counsellor_name} on {date} at {time}"
    print(message)
    return message

@tool
def send_confirmation_email(first_name: str, last_name: str, user_email: str, counsellor_name: str, date: str, time: str):
    """Send a confirmation email to a client with a counsellor at a date and time."""
    message = f"Sending confirmation email to {first_name} {last_name} ({user_email}) with {counsellor_name} on {date} at {time}"
    print(message)
    return message

tools = [book_appointment, check_availability, cancel_appointment, confirm_appointment, send_confirmation_email]
tool_by_name = {booking_tool.name: booking_tool for booking_tool in tools}

llm_with_tools = llm.bind_tools(tools)
response = llm_with_tools.invoke([
    SystemMessage(content=SYSTEM_PROMPT),
    AIMessage(content="Hello, I am the booking agent. How can I help you today?"),
    HumanMessage(content="I want to book an appointment with Dr. John Doe on 2026-11-11 at 10:00"),
])

tool_calls = response.tool_calls
print(f"Tool calls: {tool_calls}")

for tool_call in tool_calls:
    print(f"Tool name: {tool_call['name']}")
    print(f"Tool args: {tool_call['args']}")
    result = tool_by_name[tool_call["name"]].invoke(tool_call["args"])
    print(f"Tool result: {result}")
