import json
from collections import defaultdict

import streamlit as st
from langchain.chains import ConversationalRetrievalChain

from config.configuration import configs
from constants import app_constants as ac
from services import common_service as cs
from services import file_service as fs
from services import operations_service as ops
from services import streamlit_service as sts

STATIC_PROMPTS = {
    ac.FILE_TYPE_PDF: '''You are a financial analyst. Shared context is data from a financial document. Answer the query using \
the given data as knowledge base. Focus on capturing the main ideas and key points discussed in the document. Use \
your own words and ensure clarity and coherence in the response. Query: \n''',
    ac.FILE_TYPE_EXCEL: '''
For the following query, if it requires drawing a table, reply as follows:
{"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

If the query requires creating a bar chart, reply as follows:
{"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

If the query requires creating a line chart, reply as follows:
{"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

There can only be two types of chart, "bar" and "line".

If it is just asking a question that requires neither, reply just the String response.

If you do not know the answer, reply as follows: "I do not know."

Return all output as a string.

All strings in "columns" list and "data" list, should be in double quotes,
For example: For table - {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}
For bar and line - {"columns": ["Gilead", "Spider's Web"], "data": [361, 5164]}

Lets think step by step. Below is the query.
Query: '''
}

TENANT = ac.TENANT_AFG_FINANCE


def get_static_prompt(prompt_type):
    return STATIC_PROMPTS[prompt_type]


@st.cache_data(show_spinner=configs['streamlit.spinner.messages.get_allowed_file_types'])
def get_allowed_file_types():
    types = defaultdict(list)
    for file_type_config in configs['financeGPT.fileTypes']:
        types[file_type_config['name']] = file_type_config['extensions']
    return types


def run_streamlit_app():
    st.title('Finance GPT')
    assistant_avatar = sts.get_assistant_avatar(TENANT)
    user_avatar = sts.get_user_avatar(TENANT)

    llm = cs.get_llm()
    if not llm:
        print('NO ACTIVE LLM INSTANCE AVAILABLE')
        return

    file_type = sts.get_selection_from_sidebar(st, 'Select file type', get_allowed_file_types().keys())
    files = st.file_uploader(f"Upload your {file_type} document", type=get_allowed_file_types()[file_type],
                             accept_multiple_files=True)

    if files:
        if 'last_file_id' not in st.session_state or files[0].file_id != st.session_state.last_file_id:
            st.session_state.messages = []
            st.session_state.last_file_id = files[0].file_id if files else None
        qa, csv_agent = None, None
        if file_type == ac.FILE_TYPE_PDF:
            texts = fs.get_files_text(files)
            processed_data = ops.get_processed_data_from_text('\n----\n'.join(texts))
            qa = ConversationalRetrievalChain.from_llm(llm, processed_data.as_retriever())
        elif file_type == ac.FILE_TYPE_EXCEL:
            csv_agent = cs.get_csv_agent(llm, files)
        else:
            print('FILE TYPE NOT SUPPORTED')
            return

        for message in st.session_state.messages:
            role = message['role']
            with st.chat_message(role, avatar=sts.get_avatar_for_role(role, TENANT)):
                sts.write_response(st, message['content'], file_type)

        if prompt := st.chat_input('Enter your query'):
            combined_prompt = get_static_prompt(file_type) + prompt
            print(f'Combined prompt: {combined_prompt}')
            st.session_state.messages.append({'role': 'user', 'content': prompt})

            with st.chat_message('user', avatar=user_avatar):
                st.markdown(prompt)

            with st.chat_message('assistant', avatar=assistant_avatar):
                response = ops.get_prompt_result_from_context(combined_prompt, _chain=qa, _agent=csv_agent)
                sts.write_response(st, response, file_type)
            print(f'Response: {json.dumps(response)}')
            st.session_state.messages.append({'role': 'assistant', 'content': response})


run_streamlit_app()
