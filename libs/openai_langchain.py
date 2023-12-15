import traceback
import os
import streamlit as st
from langchain.chat_models import ChatLiteLLM
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from libs.logger import logger
from dotenv import load_dotenv

class OpenAILangChain:
    code_chain = None
    code_language = 'Python'
    lite_llm = None  # Change from open_ai_llm to lite_llm
    memory = None
    
    def __init__(self,code_language="python",temprature:float=0.3,max_tokens=1000,model="gpt-3.5-turbo",api_key=None):
        code_prompt = st.session_state.code_prompt
        code_language = st.session_state.code_language
        logger.info(f"Initializing OpenAILangChain... with parameters: {code_language}, {temprature}, {max_tokens}, {model} {code_prompt}")

        # Set the OPENAI_API_KEY environment variable
        load_dotenv()
        
        #st.toast(f"Proxy API value is {st.session_state.proxy_api} and length {len(st.session_state.proxy_api)}", icon="✅")
        if st.session_state.proxy_api != "" and len(st.session_state.proxy_api) > 0 and api_key == None:
            st.toast("Using proxy API", icon="✅")
            os.environ["OPENAI_API_KEY"] = "" # This value is ignored when api_base is set.
        elif api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Create a LiteLLM model
        self.lite_llm = ChatLiteLLM(model=model, temperature=temprature, max_tokens=max_tokens, openai_api_key=api_key)
        
        if st.session_state.proxy_api:
            self.lite_llm.api_base = st.session_state.proxy_api
        
        # Define code_template and memory
        code_template = PromptTemplate(input_variables=['code_prompt'],template='Write a code in ' +f'{code_language} language' + ' for {code_prompt}')
        memory = ConversationBufferMemory(input_key='code_prompt', memory_key='chat_history')
        
        # give info of selected source for API key
        if api_key:
            pass
            #st.toast("Using API key from input", icon="🔑")
        else:
            st.toast("Using API key from .env file", icon="🔑")
        
        self.code_language = code_language
        
        # Dynamically construct guidelines based on session state
        guidelines_list = []

        if st.session_state["coding_guidelines"]["modular_code"]:
            guidelines_list.append("- Ensure the method is modular in its approach.")
        if st.session_state["coding_guidelines"]["exception_handling"]:
            guidelines_list.append("- Integrate robust exception handling.")
        if st.session_state["coding_guidelines"]["error_handling"]:
            guidelines_list.append("- Add error handling to each module.")
        if st.session_state["coding_guidelines"]["efficient_code"]:
            guidelines_list.append("- Optimize the code to ensure it runs efficiently.")
        if st.session_state["coding_guidelines"]["robust_code"]:
            guidelines_list.append("- Ensure the code is robust against potential issues.")
        if st.session_state["coding_guidelines"]["naming_conventions"]:
            guidelines_list.append("- Follow standard naming conventions.")

        # Convert the list to a string
        guidelines = "\n".join(guidelines_list)

        # Setting Prompt Template.
        input_section = f"Given the input for code: {st.session_state.code_input}" if st.session_state.code_input else "make sure the program doesn't ask for any input from the user"

        template = f"""
        Task: Design a program {{code_prompt}} in {{code_language}} with the following guidelines and
        make sure the output is printed on the screen.
        And make sure the output contains only the code and nothing else.
        {input_section}

        Guidelines:
        {guidelines}
        """
        
        # Prompt Templates
        code_template = PromptTemplate(input_variables=["code_prompt", "code_language"], template=template)
        # LLM Chains definition
        
        # Create a chain that generates the code
        self.code_chain = LLMChain(llm=self.lite_llm, prompt=code_template,output_key='code', memory=memory, verbose=True)  # Change from open_ai_llm to lite_llm

        # Auto debug chain
        auto_debug_template = PromptTemplate(input_variables=['code_prompt'],template='Debug and fix any error in the following code in ' +f'{code_language} language' + ' for {code_prompt}')
        auto_debug_chain = LLMChain(llm=self.lite_llm, prompt=auto_debug_template,output_key='code_fix', memory=self.memory, verbose=True)  # Change from open_ai_llm to lite_llm
        
        if not st.session_state.auto_debug_chain:
            st.session_state.auto_debug_chain = auto_debug_chain
        
        # Create a sequential chain that combines the two chains above
        sequential_chain = SequentialChain(chains=[self.code_chain, auto_debug_chain], input_variables=['code_prompt','code_language'], output_variables=['code', 'code_fix'])
           
        # Save the chain in the session state
        if "sequential_chain" not in st.session_state:
            st.session_state.sequential_chain = sequential_chain

    def generate_code(self,code_prompt,code_language):
        try:
            
            # check for valid prompt and language
            if not code_prompt or len(code_prompt) == 0:
                st.toast("Error in code generation: Please enter a valid prompt.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt.")
                return
            
            logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
            if code_prompt and len(code_prompt) > 0 and code_language and len(code_language) > 0:
                logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
                
                if self.code_chain:
                    logger.info(f"Code chain is initialized.")
                    st.session_state.generated_code = self.code_chain.run({"code_prompt": code_prompt, "code_language": code_language})
                    logger.info(f"Generated code: {st.session_state.generated_code[:100]}...")

                # Memory for the conversation
                memory = ConversationBufferMemory(input_key='code_prompt', memory_key='chat_history')

                # save the memory in the session state
                if "memory" in st.session_state:
                    st.session_state.memory = memory
                
                #with st.expander('Message History'):
                    #st.info(memory.buffer)
                code = st.session_state.generated_code
                if '```' in code:
                    start = code.find('```') + len('```\n')
                    end = code.find('```', start)
                    # Skip the first line after ```
                    start = code.find('\n', start) + 1
                    extracted_code = code[start:end]
                    return extracted_code
                else:
                    return code

            else:
                st.toast("Error in code generation: Please enter a valid prompt and language.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt and language.")
        except Exception as e:
            st.toast(f"Error in code generation: {e}", icon="❌")
            logger.error(f"Error in code generation: {traceback.format_exc()}")