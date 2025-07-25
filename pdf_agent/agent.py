import pdfplumber
import pandas as pd

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def read_resource(pdf_path: str) -> dict:
    """
    Reads a PDF file and extracts its text, line by line.

    Args:
        pdf_path (str): Local path to the PDF file.

    Returns:
        dict:
          status (str): "success" or "error"
          lines (List[str]): extracted text lines (empty if none)
          error_message (str, optional): error details if status=="error"
    """
    try:
        data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    data.extend(text.split("\n"))
        return {"status": "success", "lines": data}
    except Exception as e:
        return {"status": "error", "lines": [], "error_message": str(e)}

# Define Agent
root_agent = Agent(
    name="Pdf_agent",
    model="gemini-2.0-flash-exp",
    description="Answer questions by reading PDF files.",
    instruction="Use the `read_resource` tool to load PDF text and then answer user queries.",
    tools=[read_resource],
)

def ask_agent(question: str, runner: Runner, user_id: str, session_id: str) -> str | None:
    """
    Sends a question to the agent and returns its final response.
    """
    content = types.Content(role="user", parts=[types.Part(text=question)])
    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)
    for event in events:
        if event.is_final_response():
            return event.content.parts[0].text
    return None

def main():
    # Set up session & runner
    session_service = InMemorySessionService()
    session_service.create_session(
        app_name="Pdf_agent", user_id="user123", session_id="sess1"
    )
    runner = Runner(
        agent=root_agent,
        app_name="Pdf_agent",
        session_service=session_service
    )

    # Ask the agent to load a PDF and count its lines
    question = "Please load data/data.pdf and tell me how many lines it has."
    answer = ask_agent(question, runner, "user123", "sess1")
    print("Agent answer:", answer)

    # Post-process the PDF as a DataFrame
    result = read_resource("data/data.pdf")
    if result["status"] == "success":
        df = pd.DataFrame(result["lines"], columns=["Extracted Text"])
        print("\nFirst 5 lines from the PDF:")
        print(df.head())
    else:
        print("Error reading PDF:", result.get("error_message"))


