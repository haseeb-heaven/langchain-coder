# langchain_coder.py

# Importing the libraries
import tempfile
import subprocess
import traceback
import sys
import os
from io import StringIO
import streamlit as st
from streamlit.components.v1 import html
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
import langchain.agents as lc_agents
from langchain.llms import OpenAI
import logging
from datetime import datetime
from langchain.llms import OpenAI as LangChainOpenAI
import openai
from dotenv import load_dotenv

class LangChainCoder:
    code_chain = None
    code_language = 'Python'
    
    def __init__(self,code_language):
        # Load the environment variables
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        memory = ConversationBufferMemory(input_key='code_topic', memory_key='chat_history')
        self.code_language = code_language
        # Prompt Templates
        code_template = PromptTemplate(input_variables=['code_topic'],template='Write me code in ' +f'{code_language} language' + ' for {code_topic}')
        
        code_fix_template = PromptTemplate(input_variables=['code_topic'],template='Fix any error in the following code in ' +f'{code_language} language' + ' for {code_topic}')
        # LLM Chains definition
        
        # Create an OpenAI LLM model
        open_ai_llm = OpenAI(temperature=0.7, max_tokens=1000)

        # Create a chain that generates the code
        self.code_chain = LLMChain(llm=open_ai_llm, prompt=code_template,
                            output_key='code', memory=memory, verbose=True)

        # Create a chain that fixes the code
        code_fix_chain = LLMChain(llm=open_ai_llm, prompt=code_fix_template,
                                output_key='code_fix', memory=memory, verbose=True)

        # Create a sequential chain that combines the two chains above
        sequential_chain = SequentialChain(chains=[self.code_chain, code_fix_chain], input_variables=[
                                        'code_topic'], output_variables=['code', 'code_fix'])
        if "sequential_chain" in st.session_state:
            st.session_state.sequential_chain = sequential_chain

    def generate_code(self,code_prompt,code_language):
        try:
            st.session_state.generated_code = self.code_chain .run(code_prompt)
            st.session_state.code_language = code_language
            st.code(st.session_state.generated_code,language=st.session_state.code_language.lower())

            # Memory for the conversation
            memory = ConversationBufferMemory(input_key='code_topic', memory_key='chat_history')

            # save the memory in the session state
            if "memory" in st.session_state:
                st.session_state.memory = memory
            
            with st.expander('Message History'):
                st.info(memory.buffer)
        except Exception as e:
            st.write(traceback.format_exc())
            logging.error(f"Error in code generation: {traceback.format_exc()}")

    def fix_code(self, code_prompt, code_language):
        # ... [code fixing logic]
        return fixed_code
