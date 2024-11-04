import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_csv_agent

from config.configuration import configs
from services import openai_service as ois
from services import sap_ai_service as sas


def get_active_ai_service():
    service = None
    if configs['sapAI.active']:
        service = sas
    elif configs['openai.active']:
        service = ois
    return service


def get_embeddings():
    service = get_active_ai_service()
    return service.get_embeddings() if service else None


@st.cache_resource(show_spinner=configs['streamlit.spinner.messages.get_llm'])
def get_llm():
    service = get_active_ai_service()
    return service.get_llm() if service else None


@st.cache_resource(show_spinner=configs['streamlit.spinner.messages.get_csv_agent'])
def get_csv_agent(_llm, csv_files):
    return create_csv_agent(
        _llm,
        csv_files,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )
