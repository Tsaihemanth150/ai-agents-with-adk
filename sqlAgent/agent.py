
from google.adk.agents import Agent
import os
import pyodbc
import dotenv

dotenv.load_dotenv()
conn_str=os.getenv("connectionString")
def sql_agent() -> str:
    try:
        # Establish connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        tables = cursor.fetchall()

        print("Tables in the database:")
        for table in tables:
            print(table[0])

        # Close the connection
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)



## Agent Config
root_agent = Agent(
    name="SQL_Agent",  ## agnet name
    model="gemini-2.0-flash-exp",  ## LLM model
    description=(
        "Agent to answer questions about the SQL database."
    ),
    instruction=(
        "I can answer your questions about the about the SQL database."
    ),  ## context
    tools=[sql_agent],  ## Tools
)
