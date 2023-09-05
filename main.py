import streamlit as st
import re
from libs.langchain_coder import LangChainCoder
from libs.codey_lib import CodeyLib
from libs.general_utils import GeneralUtils
from libs.lang_codes import LangCodes
from libs.logger import logger

general_utils = None

def initialize_session_state():
    if "code_language" not in st.session_state:
        st.session_state.code_language = "Python"
    if "compiler_mode" not in st.session_state:
        st.session_state.compiler_mode = "Online"
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "ai_option" not in st.session_state:
        st.session_state.ai_option = "Open AI"
    if "output" not in st.session_state:
        st.session_state.output = ""
        
def main():
    # initialize session state
    initialize_session_state()
    
    # Initialize classes
    code_language = st.session_state.get("code_language", "Python")
    lang_chain_coder = None # We'll initialize this after settings
    codey = None  # We'll initialize this after loading environment variables
    general_utils = GeneralUtils()
    # Streamlit UI
    st.title("LangChain Coder - AI 🦜🔗")
    logger.info("LangChain Coder - AI 🦜🔗")
    
    # Session states for input options
    ai_option = st.session_state.get("ai_option", "Open AI")
    st.session_state.code_language = st.session_state.get("code_language", "Python")
    st.session_state.compiler_mode = st.session_state.get("compiler_mode", "Online")

    # Dropdown for selecting AI options
    st.selectbox("Select an AI option", ["Open AI", "Vertex AI"], key="ai_option")

    # Dropdown for selecting code language
    st.selectbox("Select a language", list(LangCodes().keys()), key="code_language")

    # Radio buttons for selecting compiler mode
    st.radio("Compiler Mode", ("Online", "Offline"), key="compiler_mode")

    # Adding logs
    logger.info(f"AI Option: {st.session_state.ai_option}")
    logger.info(f"Code Language: {st.session_state.code_language}")
    logger.info(f"Compiler Mode: {st.session_state.compiler_mode}")
    
    # Load environment variables for Open AI
    if ai_option == "Open AI":
        with st.expander("Open AI Settings"):
            openai_api_key = st.text_input("Open AI API Key:", type="password")
            lang_chain_coder = LangChainCoder(code_language="Python", api_key=openai_api_key)
            logger.info(f"Open AI API Key: {openai_api_key}")
    
    # Load environment variables for Vertex AI
    if ai_option == "Vertex AI":
        with st.expander("Vertex AI Settings"):
            project = st.text_input("Project name:")
            region = st.text_input("App region:")
            logger.info(f"Vertex AI Project: {project} and Region: {region}")
            # add file uploader and get its file path and save to credentials_file_path.
            credential_file = st.file_uploader("Upload credentials file", type=["json"])
            if credential_file:
                credentials_file_path = credential_file.name
                
        if project and region:
            # Load environment variables
            general_utils.load_enviroment_variables(project=project, credentials_file_path=credentials_file_path, region=region)
            # Initialize CodeyLib
            codey = CodeyLib(project=project, location=region, model_name="code-bison", max_output_tokens=1024, temperature=0.1)
            codey.load_model()

    code_prompt = st.text_input("Enter a prompt to generate the code")

    if st.button("Generate Code"):
        if ai_option == "Open AI":
            st.session_state.generated_code = lang_chain_coder.generate_code(code_prompt, code_language)
        elif ai_option == "Vertex AI" and codey:
            st.session_state.generated_code  = codey.generate_code(code_prompt,code_language)
        else:
            st.error("Please select a valid AI option and fill in the required details.")
            st.session_state.generated_code  = ""
        
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code )

        # Save Code
        code_file = st.text_input("Enter file name:")
        if st.button("Save Code"):
            general_utils.save_code(code_file)

        # Run Code
        if st.button("Run Code") and st.session_state.generated_code :
            st.session_state.output = general_utils.execute_code(st.session_state.compiler_mode)

if __name__ == "__main__":
    main()