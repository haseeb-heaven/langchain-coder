"""
# LangChain Coder - AI 🦜🔗
This is all in one tools for AI based code generation and code completion. It uses Open AI and Vertex AI models for code generation and code completion. It also provides an option to save the generated code and execute it. It also provides an option to select the coding guidelines for the generated code.
it features code completion and code generation using Open AI and Vertex AI models. It also provides an option to save the generated code and execute it. It also provides an option to select the coding guidelines for the generated code.
It has code editor with advanced features like font size, tab size, theme, keybinding, line number, print margin, wrap, auto update, readonly, language.
It has more customization options for Vertex AI model like temperature, max tokens, model name, project, region, credentials file.
It has offline and online compiler mode for code execution.
It has Coding Guidelines for generated code like modular code, exception handling, error handling, logs, comments, efficient code, robust code, memory efficiency, speed efficiency, naming conventions.

Author: HeavenHM (http://www.github.com/haseeb-heaven)
Date : 06/09/2023
"""

# Install dependencies
import os
from libs.geminiai import GeminiAI
from libs.palmai import PalmAI
import streamlit as st
from libs.vertexai_langchain import VertexAILangChain
from libs.general_utils import GeneralUtils
from libs.lang_codes import LangCodes
from libs.openai_langchain import OpenAILangChain
from libs.logger import logger
from streamlit_ace import st_ace

general_utils = None

def initialize_session_state():
    if "code_language" not in st.session_state:
        st.session_state.code_language = "Python"
    if "compiler_mode" not in st.session_state:
        st.session_state.compiler_mode = "Offline"
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "ai_option" not in st.session_state:
        st.session_state.ai_option = "Open AI"
    if "output" not in st.session_state:
        st.session_state.output = ""
    if "vertex_ai_loaded" not in st.session_state:
        st.session_state.vertex_ai_loaded = False
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "project" not in st.session_state:
        st.session_state.project = ""
    if "region" not in st.session_state:
        st.session_state.region = ""
    if "vertexai_langchain" not in st.session_state:
        st.session_state.vertexai_langchain= None
    if "openai_langchain" not in st.session_state:
        st.session_state.openai_langchain = None
    if "code_prompt" not in st.session_state:
        st.session_state.code_prompt = ""
    if "display_cost" not in st.session_state:
        st.session_state.display_cost = False
    if "download_link" not in st.session_state:
        st.session_state.download_link = None
    if "download_logs" not in st.session_state:
        st.session_state.download_logs = False
    if "auto_debug_chain" not in st.session_state:
        st.session_state.auto_debug_chain = False
    if "code_input" not in st.session_state:
        st.session_state.code_input = None
    if "code_output" not in st.session_state:
        st.session_state.code_output = None
    if "palm_langchain" not in st.session_state:
        st.session_state.palm_langchain = None
    if "gemini_langchain" not in st.session_state:
        st.session_state.gemini_langchain = None
    if "code_fix_instructions" not in st.session_state:
        st.session_state.code_fix_instructions = None
    if "session_state.sequential_chain" not in st.session_state:
        st.session_state.sequential_chain = None

    # Initialize session state for Vertex AI
    if "vertexai" not in st.session_state:
        st.session_state["vertexai"] = {
            "model_name": "code-bison",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    
    # Initialize session state for Open AI
    if "openai" not in st.session_state:
        st.session_state["openai"] = {
            "model_name": "text-davinci-003",
            "temperature": 0.1,
            "max_tokens": 2048
        }
        
    # Initialize session state for Palm AI
    if "palm" not in st.session_state:
        st.session_state["palm"] = {
            "model_name": "text-bison-001",
            "temperature": 0.1,
            "max_tokens": 2048
        }

    # Initialize session state for Palm AI
    if "gemini" not in st.session_state:
        st.session_state["gemini"] = {
            "model_name": "gemini-pro",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    
    if "coding_guidelines" not in st.session_state:
        st.session_state["coding_guidelines"] = {
            "modular_code": False,
            "exception_handling": False,
            "error_handling": False,
            "logs": False,
            "comments": False,
            "efficient_code": False,
            "robust_code": False,
            "memory_efficiency": False,
            "speed_efficiency": False,
            "naming_conventions": False
        }
  
# Load the CSS files
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Load the CSS files
    load_css('static/css/styles.css')

    # initialize session state
    initialize_session_state()
    
    # Initialize classes
    code_language = st.session_state.get("code_language", "Python")
    general_utils = GeneralUtils()
    
    # Streamlit UI 
    st.title("LangChain Coder - AI 🦜🔗")
    logger.info("LangChain Coder - AI 🦜🔗")
    
    # Support
    display_support()
    
    # Sidebar for settings
    with st.sidebar:
        # Session states for input options
        st.session_state.ai_option = st.session_state.get("ai_option", "Open AI")
        st.session_state.code_language = st.session_state.get("code_language", "Python")
        st.session_state.compiler_mode = st.session_state.get("compiler_mode", "Offline")

        # Dropdown for selecting AI options
        st.selectbox("Select AI", ["Open AI", "Vertex AI", "Palm AI","Gemini AI"], key="ai_option")

        # Dropdown for selecting code language
        st.selectbox("Select language", list(LangCodes().keys()), key="code_language")

        # Radio buttons for selecting compiler mode
        st.radio("Compiler Mode", ("Online", "Offline"), key="compiler_mode")
        credentials_file_path = None
        
        # Create checkbox for Displaying cost of generated code
        with st.expander("General Settings", expanded=False):
            st.session_state.display_cost = st.checkbox("Display Cost/API", value=False)
            st.session_state.download_logs = st.checkbox("Download Logs", value=False)
            # Display the logs
            if st.session_state.download_logs:
                logs_filename = "langchain-coder.log"
                # read the logs
                with open(logs_filename, "r") as file:
                    logs_data = file.read()
                    # download the logs
                    file_format = "text/plain"
                    st.session_state.download_link = general_utils.generate_download_link(logs_data, logs_filename, file_format,True)
                
        # Setting options for Open AI
        api_key = None
        if st.session_state.ai_option == "Open AI":
            with st.expander("Open AI Settings"):
                try:
                    # Settings for Open AI model.
                    model_options_openai = ["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0301", "text-davinci-003"]
                    st.session_state["openai"]["model_name"] = st.selectbox("Model name", model_options_openai, index=model_options_openai.index(st.session_state["openai"]["model_name"]))
                    st.session_state["openai"]["temperature"] = st.slider("Temperature", min_value=0.0, max_value=2.0, value=st.session_state["openai"]["temperature"], step=0.1)
                    st.session_state["openai"]["max_tokens"] = st.slider("Maximum Tokens", min_value=1, max_value=4096, value=st.session_state["openai"]["max_tokens"], step=1)
                    
                    # Check if the API key is in App secrets.
                    if st.secrets["OPENAI_API_KEY"]:
                        api_key = st.secrets["OPENAI_API_KEY"]
                        logger.info("Gemini AI API key is initialized from App secrets.")
                    else:
                        api_key = st.text_input("API Key", value="", key="api_key", type="password")
                    
                    st.session_state.proxy_api = st.text_input("Proxy API", value="",placeholder="http://myproxy-api.replit.co/")
                    st.session_state.openai_langchain = OpenAILangChain(st.session_state.code_language, st.session_state["openai"]["temperature"], st.session_state["openai"]["max_tokens"], st.session_state["openai"]["model_name"], api_key)
                    st.toast("Open AI initialized successfully.", icon="✅")
                except Exception as exception:
                    st.toast(f"Error loading Open AI: {str(exception)}", icon="❌")
                    logger.error(f"Error loading Open AI: {str(exception)}")

        # Setting options for Vertex AI
        elif st.session_state.ai_option == "Vertex AI":
            try:
                with st.expander("Vertex AI Settings"):
                    try:
                        # Settings for Vertex AI model.
                        st.session_state.project = st.text_input("Project:")
                        st.session_state.region = st.text_input("Region:")
                        st.session_state.uploaded_file = st.file_uploader("Service account file", type=["json"])
                        st.session_state["vertexai"]["temperature"] = st.slider("Temperature", min_value=0.0, max_value=2.0, value=st.session_state["vertexai"]["temperature"], step=0.1)
                        st.session_state["vertexai"]["max_tokens"] = st.slider("Maximum Tokens", min_value=1, max_value=4096, value=st.session_state["vertexai"]["max_tokens"], step=1)
                        model_options_vertex = ["code-bison", "code-gecko"]
                        st.session_state["vertexai"]["model_name"] = st.selectbox("Model", model_options_vertex, index=model_options_vertex.index(st.session_state["vertexai"]["model_name"]))
                        logger.info(f"Vertex AI Project: {st.session_state.project} and Region: {st.session_state.region}")
                        
                    except Exception as exception:
                        logger.error(f"Error loading Vertex AI: {str(exception)}")
                        st.toast(f"Error loading Vertex AI: {str(exception)}", icon="❌")
                        
                        logger.info("Vertex AI project and region selected.")
                        st.toast("Vertex AI project and region selected.", icon="✅")
                        
                    if st.session_state.uploaded_file:
                        logger.info(f"Vertex AI File credentials file '{st.session_state.uploaded_file.name}' initialized state {st.session_state.vertex_ai_loaded}")         
                        # Save the temorary uploaded file and delete it after 60 seconds due to security reasons. (Credentials file is deleted after 60 seconds)
                        file_path = general_utils.save_uploaded_file_temp(st.session_state.uploaded_file)  # Save the uploaded file
                        if file_path:
                            credentials_file_path = file_path
                        else:
                            st.toast("Failed to save the uploaded file.", icon="❌")
                    
                    if st.session_state.project and st.session_state.region and st.session_state.uploaded_file:
                        try:
                            # Initialize vertex ai model
                            if not st.session_state.vertex_ai_loaded:
                                st.session_state.vertexai_langchain= VertexAILangChain(project=st.session_state.project, location=st.session_state.region, model_name=st.session_state["vertexai"]["model_name"], max_tokens=st.session_state["vertexai"]["max_tokens"], temperature=st.session_state["vertexai"]["temperature"], credentials_file_path=credentials_file_path)
                                st.session_state.vertex_ai_loaded = st.session_state.vertexai_langchain.load_model(st.session_state["vertexai"]["model_name"],st.session_state["vertexai"]["max_tokens"],st.session_state["vertexai"]["temperature"])
                                st.toast("Vertex AI initialized successfully.", icon="✅")
                        except Exception as exception:
                            st.toast(f"Error loading Vertex AI: {str(exception)}", icon="❌")
                            logger.error(f"Error loading Vertex AI: {str(exception)}")
                    else:
                        # Define a dictionary mapping variable names
                        items = {
                            'st.session_state.project': 'Project name',
                            'st.session_state.region': 'App region',
                            'st.session_state.uploaded_file': 'Credentials file'
                        }

                        # Use a list comprehension to filter out the unset items
                        unset_items = [name for var, name in items.items() if not eval(var)]

                        # Construct the error message
                        error_message = "Please select all settings for Vertex AI".join([f"{item} is not selected." for item in unset_items])
                                                
                        # Show error message
                        st.toast(error_message, icon="❌")
                        logger.error(error_message)
            
            except Exception as exception:
                st.toast(f"Error loading Vertex AI: {str(exception)}", icon="❌")
                logger.error(f"Error loading Vertex AI: {str(exception)}")
                
        # Setting options for Palm AI
        elif st.session_state.ai_option == "Palm AI":
            with st.expander("Palm AI Settings"):
                try:
                    # Settings for Palm AI model.
                    model_options_palm = ["chat-bison-001", "text-bison-001", "embedding-gecko-001"]
                    st.session_state["palm"]["model_name"] = st.selectbox("Model name", model_options_palm, index=model_options_palm.index(st.session_state["palm"]["model_name"]))
                    st.session_state["palm"]["temperature"] = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state["palm"]["temperature"], step=0.1)
                    st.session_state["palm"]["max_tokens"] = st.slider("Maximum Tokens", min_value=1, max_value=8196, value=st.session_state["palm"]["max_tokens"], step=1)
                    
                    # Check if the API key is in App secrets.
                    if st.secrets["PALM_API_KEY"]:
                        api_key = st.secrets["PALM_API_KEY"]
                        logger.info("Gemini AI API key is initialized from App secrets.")
                    else:
                        # Add password option for getting API key
                        api_key = st.text_input("API Key", type="password")
                    try:
                        st.session_state.palm_langchain = PalmAI(api_key, model=st.session_state["palm"]["model_name"], temperature=st.session_state["palm"]["temperature"], max_output_tokens=st.session_state["palm"]["max_tokens"])
                    except Exception as exception:
                        st.toast(f"Error initializing PalmAI: {str(exception)}", icon="❌")
                        logger.error(f"Error initializing PalmAI: {str(exception)}")
                    st.toast("Palm AI initialized successfully.", icon="✅")
                except Exception as exception:
                    st.toast(f"Error loading Palm AI: {str(exception)}", icon="❌")
                    logger.error(f"Error loading Palm AI: {str(exception)}")
    
        # Setting options for Gemini AI
        elif st.session_state.ai_option == "Gemini AI":
            with st.expander("Gemini AI Settings"):
                try:
                    # Settings for Gemini AI model.
                    model_options_gemini = ["gemini-pro","gemini-pro-vision"]
                    st.session_state["gemini"]["model_name"] = st.selectbox("Model name", model_options_gemini, index=model_options_gemini.index(st.session_state["gemini"]["model_name"]))
                    st.session_state["gemini"]["temperature"] = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state["gemini"]["temperature"], step=0.1)
                    st.session_state["gemini"]["max_tokens"] = st.slider("Maximum Tokens", min_value=1, max_value=8196, value=st.session_state["gemini"]["max_tokens"], step=1)

                    # Check if the API key is in App secrets.
                    if st.secrets["GEMINI_API_KEY"]:
                        api_key = st.secrets["GEMINI_API_KEY"]
                        logger.info("Gemini AI API key is initialized from App secrets.")
                    else:
                        # Add password option for getting API key
                        api_key = st.text_input("API Key", type="password")
                        logger.info("Gemini AI API key is initialized from user input.")
                    try:
                        st.session_state.gemini_langchain = GeminiAI(api_key, model=st.session_state["gemini"]["model_name"], temperature=st.session_state["gemini"]["temperature"], max_output_tokens=st.session_state["gemini"]["max_tokens"])
                    except Exception as exception:
                        st.toast(f"Error initializing Gemini AI: {str(exception)}", icon="❌")
                        logger.error(f"Error initializing Gemini AI: {str(exception)}")
                    st.toast("Gemini AI initialized successfully.", icon="✅")
                except Exception as exception:
                    st.toast(f"Error loading Gemini AI: {str(exception)}", icon="❌")
                    logger.error(f"Error loading Gemini AI: {str(exception)}")
                    
    # UI Elements - Main Page
    vertex_model_selected = st.session_state["vertexai"]["model_name"]
    if vertex_model_selected == "code-bison":
        placeholder = "Enter your prompt for code generation."
    elif vertex_model_selected == "code-gecko":
        placeholder = "Enter your code for code completion."
    else:
        placeholder = "Enter your prompt for code generation."
        st.error(f"Invalid Vertex AI model selected: {vertex_model_selected}")
    
    # Input box for entering the prompt
    st.session_state.code_prompt = st.text_area("Enter Prompt", height=200, placeholder=placeholder,label_visibility='hidden')

    with st.expander("Input Options"):
        with st.container():
            st.session_state.code_input = st.text_input("Input (Stdin)", placeholder="Input (Stdin)", label_visibility='collapsed',value=st.session_state.code_input)
            st.session_state.code_output = st.text_input("Output (Stdout)", placeholder="Output (Stdout)", label_visibility='collapsed',value=st.session_state.code_output)
            st.session_state.code_fix_instructions = st.text_input("Fix instructions", placeholder="Fix instructions", label_visibility='collapsed',value=st.session_state.code_fix_instructions)

    # Set the input and output to None if the input and output is empty
    if st.session_state.code_input and st.session_state.code_output: 
        if len(st.session_state.code_input) == 0:
            st.session_state.code_input = None
            logger.info("Stdin is empty.")
        else:
            logger.info(f"Stdin: {st.session_state.code_input}")
        if len(st.session_state.code_output) == 0:
            st.session_state.code_output = None
            logger.info("Stdout is empty.")
        else:
            logger.info(f"Stdout: {st.session_state.code_output}")
    
                
    with st.form('code_controls_form'):
        # Create columns for alignment
        file_name_col, save_code_col,generate_code_col,run_code_col,fix_code_col = st.columns(5)

        # Input Box (for entering the file name) in the first column
        with file_name_col:
            code_file = st.text_input("File name", value="", placeholder="File name", label_visibility='collapsed')

        # Save Code button in the second column
        with save_code_col:
            download_code_submitted = st.form_submit_button("Download")
            if download_code_submitted:
                file_format = "text/plain"
                st.session_state.download_link = general_utils.generate_download_link(st.session_state.generated_code, code_file,file_format,True)
                
        # Generate Code button in the third column
        with generate_code_col:
            button_label = "Generate" if st.session_state["vertexai"]["model_name"] == "code-bison" else "Complete"
            generate_submitted = st.form_submit_button(button_label)
            
            if generate_submitted:
                if st.session_state.ai_option == "Open AI":
                    if st.session_state.openai_langchain:
                        st.session_state.generated_code = st.session_state.openai_langchain.generate_code(st.session_state.code_prompt, code_language)
                    else:# Reinitialize the chain
                        if not api_key:
                            st.toast("Open AI API key is not initialized.", icon="❌")
                            logger.error("Open AI API key is not initialized.")
                        else:
                            st.session_state.openai_langchain = OpenAILangChain(st.session_state.code_language,st.session_state["openai"]["temperature"],st.session_state["openai"]["max_tokens"],st.session_state["openai"]["model_name"],api_key)
                            st.session_state.generated_code = st.session_state.openai_langchain.generate_code(st.session_state.code_prompt, code_language)
                elif st.session_state.ai_option == "Vertex AI":
                    if st.session_state.vertexai_langchain:
                        if not st.session_state.vertex_ai_loaded:
                            st.toast("Vetex AI is not initialized.", icon="❌")
                            logger.error("Vetex AI is not initialized.")
                            return
                        if st.session_state["vertexai"]["model_name"] == "code-bison":
                            st.session_state.generated_code = st.session_state.vertexai_langchain.generate_code(st.session_state.code_prompt, code_language)
                        else:
                            st.session_state.generated_code = st.session_state.vertexai_langchain.generate_code_completion(st.session_state.code_prompt, code_language)
                    else: # Reinitalize the chain
                        st.session_state.vertexai_langchain= VertexAILangChain(project=st.session_state.project, location=st.session_state.region, model_name=st.session_state["vertexai"]["model_name"], max_tokens=st.session_state["vertexai"]["max_tokens"], temperature=st.session_state["vertexai"]["temperature"], credentials_file_path=credentials_file_path)
                        st.session_state.vertex_ai_loaded = st.session_state.vertexai_langchain.load_model(st.session_state["vertexai"]["model_name"],st.session_state["vertexai"]["max_tokens"],st.session_state["vertexai"]["temperature"])
                        st.session_state.generated_code = st.session_state.vertexai_langchain.generate_code(st.session_state.code_prompt, code_language)
                
                elif st.session_state.ai_option == "Palm AI":
                    if st.session_state.palm_langchain:
                        st.session_state.generated_code = st.session_state.palm_langchain.generate_code(st.session_state.code_prompt, code_language)
                    else:# Reinitialize the chain
                        if not api_key:
                            st.toast("Palm AI API key is not initialized.", icon="❌")
                            logger.error("Palm AI API key is not initialized.")
                        else:
                            st.session_state.palm_langchain = PalmAI(api_key, model=st.session_state["palm"]["model_name"], temperature=st.session_state["palm"]["temperature"], max_output_tokens=st.session_state["palm"]["max_tokens"])
                            st.session_state.generated_code = st.session_state.palm_langchain.generate_code(st.session_state.code_prompt, code_language)
            
                elif st.session_state.ai_option == "Gemini AI":
                    if st.session_state.gemini_langchain:
                        st.session_state.generated_code = st.session_state.gemini_langchain.generate_code(st.session_state.code_prompt, code_language)
                    else:# Reinitialize the chain
                        if not api_key:
                            st.toast("Gemini AI API key is not initialized.", icon="❌")
                            logger.error("Gemini AI API key is not initialized.")
                        else:
                            st.session_state.gemini_langchain = GeminiAI(api_key, model=st.session_state["gemini"]["model_name"], temperature=st.session_state["gemini"]["temperature"], max_output_tokens=st.session_state["gemini"]["max_tokens"])
                            st.session_state.generated_code = st.session_state.gemini_langchain.generate_code(st.session_state.code_prompt, code_language)
                
                else:
                    st.toast(f"Please select a valid AI option selected '{st.session_state.ai_option}' option", icon="❌")
                    st.session_state.generated_code = ""
                    logger.error(f"Please select a valid AI option selected '{st.session_state.ai_option}' option")

        # Fix Code button in the fourth column
        with fix_code_col:
            fix_submitted = st.form_submit_button("Auto Fix")
            if fix_submitted:
                if len(st.session_state.code_fix_instructions) == 0:
                    st.toast("Missing fix instructions", icon="❌")
                    logger.warning("Missing fix instructions")
                    
                logger.info(f"Fixing code with instructions: {st.session_state.code_fix_instructions}")
                st.session_state.generated_code = st.session_state.palm_langchain.fix_generated_code(st.session_state.generated_code, st.session_state.code_language,st.session_state.code_fix_instructions)


        # Run Code button in the fourth column
        with run_code_col:
            execute_submitted = st.form_submit_button("Execute")
            if execute_submitted:
                st.session_state.output = general_utils.execute_code(st.session_state.compiler_mode)
            
    # Save and Run Code
    if st.session_state.generated_code:
        
        # Sidebar for settings
        with st.sidebar.expander("Code Editor Settings", expanded=False):

            # Font size setting
            font_size = st.slider("Font Size", min_value=8, max_value=30, value=14, step=1)

            # Tab size setting
            tab_size = st.slider("Tab Size", min_value=2, max_value=8, value=4, step=1)

            # Theme setting
            themes = ["monokai", "github", "tomorrow", "kuroir", "twilight", "xcode", "textmate", "solarized_dark", "solarized_light", "terminal"]
            theme = st.selectbox("Theme", options=themes, index=themes.index("solarized_dark"))

            # Keybinding setting
            keybindings = ["emacs", "sublime", "vim", "vscode"]
            keybinding = st.selectbox("Keybinding", options=keybindings, index=keybindings.index("sublime"))

            # Other settings
            show_gutter = st.checkbox("Line Number", value=True)
            show_print_margin = st.checkbox("Print Margin", value=True)
            wrap = st.checkbox("Wrap", value=True)
            auto_update = st.checkbox("Auto Update", value=False)
            readonly = st.checkbox("Readonly", value=False)
            language = st.selectbox("Language", options=list(LangCodes().keys()), index=list(LangCodes().keys()).index("Python"))
            
        # Display the st_ace code editor with the selected settings
        display_code_editor(font_size, tab_size, theme, keybinding, show_gutter, show_print_margin, wrap, auto_update, readonly, language)

        # Display the code output
        if st.session_state.output:
            st.markdown("### Output")
            #st.toast(f"Compiler mode selected '{st.session_state.compiler_mode}'", icon="✅")
            if (st.session_state.compiler_mode.lower() == "offline"):
                if "https://www.jdoodle.com/plugin" in st.session_state.output:
                    pass
                else:
                    st.code(st.session_state.output, language=st.session_state.code_language.lower())
        
        # Display the price of the generated code.
        if st.session_state.generated_code and st.session_state.display_cost:
            if st.session_state.ai_option == "Open AI":
                selected_model = st.session_state["openai"]["model_name"]
                if selected_model == "gpt-3":
                    cost, cost_per_whole_string, total_cost = general_utils.gpt_3_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
                elif selected_model == "gpt-4":
                    cost, cost_per_whole_string, total_cost = general_utils.gpt_4_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
                elif selected_model == "text-davinci-003":
                    cost, cost_per_whole_string, total_cost = general_utils.gpt_text_davinci_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
            
            elif st.session_state.ai_option == "Vertex AI":
                selected_model = st.session_state["vertexai"]["model_name"]
                if selected_model == "code-bison" or selected_model == "code-gecko":
                    cost, cost_per_whole_string, total_cost = general_utils.codey_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
            
            elif st.session_state.ai_option == "Palm AI":
                selected_model = st.session_state["palm"]["model_name"]
                if selected_model == "text-bison-001":
                    cost = 0.00025  # Cost per 1K input characters for online requests
                    cost_per_whole_string = 0.0005  # Cost per 1K output characters for online requests
                    total_cost = general_utils.palm_text_bison_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
                elif selected_model == "chat-bison-001":
                    cost = 0.00025  # Cost per 1K input characters for online requests
                    cost_per_whole_string = 0.0005  # Cost per 1K output characters for online requests
                    total_cost = general_utils.palm_chat_bison_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])
                elif selected_model == "embedding-gecko-001":
                    cost = 0.0002  # Cost per 1K characters input for generating embeddings using text as an input
                    cost_per_whole_string = 0.0002  # Assuming the same cost for output characters
                    total_cost = general_utils.palm_embedding_gecko_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Token", f"{cost} USD"], ["Cost/Whole String", f"{cost_per_whole_string} USD"], ["Total Cost", f"{total_cost} USD"]])

            elif st.session_state.ai_option == "Gemini AI":
                selected_model = st.session_state["gemini"]["model_name"]
                
                if selected_model == "gemini-pro":
                    cost_per_input_char = 0.00025  # Cost per 1K input characters for online requests
                    cost_per_output_char = 0.0005  # Cost per 1K output characters for online requests
                    total_cost = general_utils.gemini_pro_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/1K Input Token", f"{cost_per_input_char} USD"], ["Cost/1K Output Token", f"{cost_per_output_char} USD"], ["Total Cost", f"{total_cost} USD"]])
                
                elif selected_model == "gemini-pro-vision":
                    cost_per_image = 0.0025  # Cost per image for online requests
                    cost_per_second = 0.002  # Cost per second for online requests
                    cost_per_input_char = 0.00025  # Cost per 1K input characters for online requests
                    cost_per_output_char = 0.0005  # Cost per 1K output characters for online requests
                    total_cost = general_utils.gemini_pro_vision_generation_cost(st.session_state.generated_code)
                    st.table([["Cost/Image", f"{cost_per_image} USD"], ["Cost/Second", f"{cost_per_second} USD"], ["Cost/1K Input Token", f"{cost_per_input_char} USD"], ["Cost/1K Output Token", f"{cost_per_output_char} USD"], ["Total Cost", f"{total_cost} USD"]])
                
    # Expander for coding guidelines
    with st.sidebar.expander("Coding Guidelines"):
        # create checkbox to select all guidelines and change the state of all guidelines
        select_all_guidelines = st.checkbox("Select All", value=False)
        if select_all_guidelines:
            for key in st.session_state["coding_guidelines"]:
                st.session_state["coding_guidelines"][key] = True
                    
        guidelines = [
            "Modular Code",
            "Exception handling",
            "Error handling",
            "Logs",
            "Comments",
            "Efficient code",
            "Robust Code",
            "Memory efficiency",
            "Speed efficiency",
            "Standard Naming conventions"
        ]

        for guideline in guidelines:
            st.session_state["coding_guidelines"][guideline.lower().replace(" ", "_")] = st.checkbox(guideline)
    
def display_code_editor(font_size, tab_size, theme, keybinding, show_gutter, show_print_margin, wrap, auto_update, readonly, language):
    if st.session_state.generated_code and st.session_state.compiler_mode == "Offline":
        st.session_state.generated_code = st_ace(
            language=language.lower(),
            theme=theme,
            keybinding=keybinding,
            height=400,
            value=st.session_state.generated_code,
            font_size=font_size,
            tab_size=tab_size,
            show_gutter=show_gutter,
            show_print_margin=show_print_margin,
            wrap=wrap,
            auto_update=auto_update,
            readonly=readonly
        )
    elif st.session_state.generated_code and st.session_state.compiler_mode == "Online":
        st.components.v1.html(st.session_state.output,width=720, height=800, scrolling=True)


def handle_onchange_vertexai_temperature(value):
    st.session_state["vertexai"]["temperature"] = value
    logger.info(f"Vertex AI temperature: {value}")
    st.toast(f"Vertex AI temperature: {value}", icon="✅")
    if st.session_state.vertexai_langchain:
        st.session_state.vertexai_langchain.set_temperature(value)
    
def handle_onchange_vertexai_tokens(value):
    st.session_state["vertexai"]["max_tokens"] = value
    logger.info(f"Vertex AI max_tokens: {value}")
    st.toast(f"Vertex AI max_tokens: {value}", icon="✅")
    if st.session_state.vertexai_langchain:
        st.session_state.vertexai_langchain.set_max_tokens(value)
    
def handle_onchange_vertexai_model(value):
    st.session_state["vertexai"]["model_name"] = value
    logger.info(f"Vertex AI model_name: {value}")
    st.toast(f"Vertex AI model_name: {value}", icon="✅")
    if st.session_state.vertexai_langchain:
        st.session_state.vertexai_langchain.set_model_name(value)

def display_support():
    st.markdown("<div style='text-align: center;'>Share and Support</div>", unsafe_allow_html=True)
    
    st.write("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <ul style="list-style-type: none; margin: 0; padding: 0; display: flex;">
                <li style="margin-right: 10px;"><a href="https://twitter.com/haseeb_heaven" target="_blank"><img src="https://img.icons8.com/color/32/000000/twitter--v1.png"/></a></li>
                <li style="margin-right: 10px;"><a href="https://www.buymeacoffee.com/haseebheaven" target="_blank"><img src="https://img.icons8.com/color/32/000000/coffee-to-go--v1.png"/></a></li>
                <li style="margin-right: 10px;"><a href="https://www.youtube.com/@HaseebHeaven/videos" target="_blank"><img src="https://img.icons8.com/color/32/000000/youtube-play.png"/></a></li>
                <li><a href="https://github.com/haseeb-heaven/LangChain-Coder" target="_blank"><img src="https://img.icons8.com/color/32/000000/github--v1.png"/></a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# create method to upgrade the pip packages and pip
def upgrade_pip_packages():
    try:
        # upgrade pip
        os.system("python -m pip install --upgrade pip")
        # upgrade pip packages
        os.system("pip install -r requirements.txt --upgrade")
    except Exception as e:
        print(f"Error upgrading pip packages: {e}")

if __name__ == "__main__":
    main()
