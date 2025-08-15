import os
from pathlib import Path
import tempfile

import streamlit as st

from sqlalchemy import inspect as sa_inspect ,create_engine

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents import AgentType
from langchain_groq import ChatGroq

# ─────────────────────────────────────────────────────────────────────────────
# Streamlit Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LangChain : Advanced AI SQL App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 LangChain : Advanced AI SQL App")

st.markdown(
    """
- Use **plain English or Urdu** to ask questions about your data.  
- Supports both **MySQL** and **SQLite**.  
- No SQL skills required — let the AI handle everything.
"""
)

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar: DB selection + credentials + API key
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("1️⃣ Database Connection Setup", divider="rainbow")
    st.markdown(
        "Select your data source below. Database credentials are handled **securely**."
    )

    DB_MODE = st.radio(
        "Database Type",
        [
            "SQLite3 (.db file : quick, demo, local analysis)",
            "MySQL (remote, enterprise, production)",
        ],
    )

    uploaded_db = None
    mysql_host = mysql_port = mysql_user = mysql_password = mysql_db = None

    if DB_MODE.startswith("SQLite"):
        st.markdown(
            """
- Upload your own SQLite **.db** file  
- Useful if you receive files from clients or other teams  
- File remains on your system, never sent to third parties
"""
        )
        uploaded_db = st.file_uploader("Upload .db file", type=["db", "sqlite"])
    else:
        st.subheader("MySQL Database Credentials")
        mysql_host = st.text_input(
            "Host", value="127.0.0.1", help="Usually 127.0.0.1 (localhost) or server IP."
        )
        mysql_port = st.text_input("Port", value="3306", help="Default port is 3306.")
        mysql_user = st.text_input("Username", value="appuser", help="Provided by DBA.")
        mysql_password = st.text_input("Password", type="password", help="Keep it safe.")
        mysql_db = st.text_input("Database Name", value="student", help="Target DB name.")

    st.divider()
    st.header("2️⃣ AI Model (Groq / Gemma)")
    st.markdown(
        """
Enter your **Groq API key** below. This key is required to use the Gemma-based model for question → SQL conversion.

- Get a free key at: https://console.groq.com/playground  
- Your data is only used to generate queries; it is not stored.
"""
    )
    groq_key = st.text_input("Groq API Key", type="password")

    st.divider()
    st.header("3️⃣ Learning & Docs")
    st.markdown(
        """
- LangChain SQL: https://python.langchain.com/docs/integrations/tools/sql_database/  
- Groq (Gemma): https://console.groq.com/playground  
- SQLAlchemy: https://docs.sqlalchemy.org/en/20/  
- SQLite3: https://docs.python.org/3/library/sqlite3.html  
- Streamlit: https://streamlit.io/
"""
    )
    st.divider()
    st.markdown("For feedback: email at info@Agent.ai")

if not groq_key:
    st.warning("Please provide your Groq API Key in the sidebar to activate AI chat features.")
    st.stop()

os.environ["GROQ_API_KEY"] = groq_key

# ─────────────────────────────────────────────────────────────────────────────
# DB Connection (robust handling)
# ─────────────────────────────────────────────────────────────────────────────
connection_success = False
connection_error = ""
sample_tables = []

engine = None
db_uri = None

try:
    if DB_MODE.startswith("SQLite"):
        # If user uploaded a db, save it to a temp file; otherwise try to use local student.db
        if uploaded_db is not None:
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
            t.write(uploaded_db.read())
            t.flush()
            t.close()
            db_file_path = t.name
        else:
            default_db = (Path(__file__).parent / "student.db")
            if not default_db.exists():
                st.warning("No default **student.db** found. Please upload a SQLite .db file.")
                st.stop()
            db_file_path = str(default_db)

        db_uri = f"sqlite:///{db_file_path}"
        engine = create_engine(db_uri, connect_args={"check_same_thread": False})

    else:
        # Build a proper MySQL URI (string, not a set)
        db_uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
        engine = create_engine(db_uri, connect_args={"auth_plugin": "mysql_native_password"})

    # Inspect tables
    inspector = sa_inspect(engine)
    sample_tables = inspector.get_table_names()
    connection_success = True

except Exception as e:
    connection_success = False
    connection_error = str(e)
    st.error(f"❌ Database connection failed! Reason: {connection_error}")

if connection_success:
    with st.sidebar:
        st.success("✅ Database connection successful. Ready to chat.")
        st.markdown(
            f"**Detected Tables:** {', '.join(sample_tables) if sample_tables else 'No tables found.'}"
        )

# ─────────────────────────────────────────────────────────────────────────────
# LangChain SQLDatabase with cache
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(ttl=3600)
def get_sql_database(uri: str) -> SQLDatabase:
    return SQLDatabase.from_uri(uri)

if not connection_success:
    st.stop()

db = get_sql_database(db_uri)

# ─────────────────────────────────────────────────────────────────────────────
# LLM & Agent (using create_sql_agent)
# ─────────────────────────────────────────────────────────────────────────────
llm = ChatGroq(model_name="gemma2-9b-it", temperature=0, streaming=True)

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# UI: Chat + Helpers
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.subheader("💬 Chat with Database (AI Powered)")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("Show All Table Names"):
        st.info(f"Tables: {', '.join(sample_tables) if sample_tables else 'No tables found.'}")

with col2:
    sample_query = st.text_input(
        "Sample Query (You can use, edit, or get ideas from this):",
        value="Show all students with marks > 80",
        help="Try: 'Total students in Karachi?', 'How many students passed?', 'List girls who scored above 85'.",
    )
    if st.button("Send Sample Query"):
        st.session_state["chat_input"] = sample_query

st.markdown("**Pro Tip:** You can ask in English or Roman Urdu e.g., 'Multan ke tamam students dikhao'.")

if st.checkbox("Show Database Schema (Tables & Columns)", value=False):
    try:
        inspector = sa_inspect(engine)
        schema = {t: [c["name"] for c in inspector.get_columns(t)] for t in sample_tables}
        st.json(schema)
    except Exception as e:
        st.error(f"Schema extraction failed: {e}")

# Chat history init / clear
if "messages" not in st.session_state or st.sidebar.button(
    "Clear History", help="Wipes entire chat history for privacy or new session."
):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome! Please ask any question about your database."}
    ]

# Render previous messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for new query
query = st.chat_input("Ask your question about the database...", key="chat_input")

# Handle query
if query:
    st.session_state["messages"].append({"role": "user", "content": query})
    st.chat_message("user").write(query)

    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        # NOTE: `invoke` returns a dict with "output" for AgentExecutor, or a string for some versions.
        result = agent_executor.invoke({"input": query}, config={"callbacks": [callback]})
        answer = result["output"] if isinstance(result, dict) and "output" in result else str(result)
        st.write(answer)
        st.session_state["messages"].append({"role": "assistant", "content": answer})


## AI Data Agent
#AI Dashboard
##Data to insights app



