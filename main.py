import os
import tempfile
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
        st.session_state.compiler_mode = "Online"
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
    if "codey" not in st.session_state:
        st.session_state.codey = None
    if "lang_chain_coder" not in st.session_state:
        st.session_state.lang_chain_coder = None
    if "codey_model_name" not in st.session_state:
        st.session_state.codey_model_name = "code-bison"
    if "code_prompt" not in st.session_state:
        st.session_state.code_prompt = ""
    
    if "openai" not in st.session_state:
        st.session_state["openai"] = {
            "model_name": "gpt-3",
            "temperature": 0.7,
            "max_tokens": 1000
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

def main():
    # initialize session state
    initialize_session_state()
    
    # Initialize classes
    code_language = st.session_state.get("code_language", "Python")
    general_utils = GeneralUtils()
    
    # Streamlit UI
    st.title("LangChain Coder - AI 🦜🔗")
    logger.info("LangChain Coder - AI 🦜🔗")
    
    # Sidebar for settings
    with st.sidebar:
        # Session states for input options
        st.session_state.ai_option = st.session_state.get("ai_option", "Open AI")
        st.session_state.code_language = st.session_state.get("code_language", "Python")
        st.session_state.compiler_mode = st.session_state.get("compiler_mode", "Online")

        # Dropdown for selecting AI options
        st.selectbox("Select AI", ["Open AI", "Vertex AI"], key="ai_option")

        # Dropdown for selecting code language
        st.selectbox("Select language", list(LangCodes().keys()), key="code_language")

        # Radio buttons for selecting compiler mode
        st.radio("Compiler Mode", ("Online", "Offline"), key="compiler_mode")
        credentials_file_path = None
        
        # Setting options for Open AI
        if st.session_state.ai_option == "Open AI":
            with st.expander("Open AI Settings"):
                try:
                    # Settings for Open AI model.
                    st.session_state["openai"]["model_name"] = st.selectbox("Select a model name", ["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613","gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0301", "text-davinci-003"])
                    st.session_state["openai"]["temperature"] = st.slider("Temprature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)
                    st.session_state["openai"]["max_tokens"] = st.slider("Maximum Tokens", min_value=1, max_value=4096, value=256, step=1)
                    api_key = st.text_input("API Key", value="", key="api_key", type="password")
                    st.session_state.lang_chain_coder = OpenAILangChain(st.session_state.code_language,st.session_state["openai"]["temperature"],st.session_state["openai"]["max_tokens"],st.session_state["openai"]["model_name"],api_key)
                except Exception as exception:
                    st.toast(f"Error loading Open AI: {str(exception)}", icon="❌")
                    logger.error(f"Error loading Open AI: {str(exception)}")
                    
        # Setting options for Vertex AI
        elif st.session_state.ai_option == "Vertex AI":
            with st.expander("Vertex AI Settings"):
                try:
                    st.session_state.project = st.text_input("Project name:", value="heavenllm")
                    st.session_state.region = st.text_input("App region:", value="us-central1")
                    st.session_state.uploaded_file = st.file_uploader("Upload Service Account Key", type=["json"])
                    # create dropdown for selecting model name listed code-bison and code-gecko
                    st.session_state.codey_model_name = st.selectbox("Select a model name", ["code-bison", "code-gecko"])
                    logger.info(f"Vertex AI Project: {st.session_state.project} and Region: {st.session_state.region}")
                    if st.session_state.uploaded_file:
                        logger.info(f"Vertex AI File credentials file '{st.session_state.uploaded_file.name}' initialized state {st.session_state.vertex_ai_loaded}")         
                        file_path = save_uploaded_file(st.session_state.uploaded_file)  # Save the uploaded file
                        if file_path:
                            credentials_file_path = file_path
                            #st.toast(f"Credentials file uploaded {credentials_file_path}", icon="✅")
                        else:
                            st.toast("Failed to save the uploaded file.", icon="❌")
                    
                    if st.session_state.project and st.session_state.region and st.session_state.uploaded_file:
                        try:
                            # Initialize CodeyLib
                            if not st.session_state.vertex_ai_loaded:
                                st.session_state.codey = VertexAILangChain(project=st.session_state.project, location=st.session_state.region, model_name=st.session_state.codey_model_name, max_output_tokens=1024, temperature=0.1, credentials_file_path=credentials_file_path)
                                st.session_state.vertex_ai_loaded = st.session_state.codey.load_model()
                                st.toast("Vertex AI initialized successfully.", icon="✅")
                        except Exception as exception:
                            st.toast(f"Error loading Vertex AI: {str(exception)}", icon="❌")
                            logger.error(f"Error loading Vertex AI: {str(exception)}")
                    else:
                        # Define a dictionary mapping variable names to their human-readable counterparts
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
    # UI Elements - Main Page
    st.session_state.code_prompt = st.text_area(" ", height=200, placeholder="Prompt to generate the code")

    with st.form('code_input_form'):
        # Create columns for alignment
        file_name_col, save_code_col, generate_code_col, run_code_col = st.columns(4)

        # `code_file` Input Box (for entering the file name) in the first column
        with file_name_col:
            code_file = st.text_input("", value="", placeholder="File name", label_visibility='collapsed')

        # Save Code button in the second column
        with save_code_col:
            save_submitted = st.form_submit_button("Save File")
            if save_submitted:
                general_utils.save_code(code_file)

        # Generate Code button in the third column
        with generate_code_col:
            generate_submitted = st.form_submit_button("Generate Code")
            if generate_submitted:
                if st.session_state.ai_option == "Open AI":
                    if st.session_state.lang_chain_coder:
                        st.session_state.generated_code = st.session_state.lang_chain_coder.generate_code(st.session_state.code_prompt, code_language)
                    else:# Reinitialize the chain
                         st.session_state.lang_chain_coder = OpenAILangChain(st.session_state.code_language,st.session_state["openai"]["temperature"],st.session_state["openai"]["max_tokens"],st.session_state["openai"]["model_name"],api_key)
                         st.session_state.generated_code = st.session_state.lang_chain_coder.generate_code(st.session_state.code_prompt, code_language)
                elif st.session_state.ai_option == "Vertex AI" and st.session_state.vertex_ai_loaded:
                    if st.session_state.codey:
                        st.session_state.generated_code = st.session_state.codey.generate_code(st.session_state.code_prompt, code_language)
                    else: # Reinitalize the chain
                        st.session_state.codey = VertexAILangChain(project=st.session_state.project, location=st.session_state.region, model_name=st.session_state.codey_model_name, max_output_tokens=1024, temperature=0.1, credentials_file_path=credentials_file_path)
                        st.session_state.vertex_ai_loaded = st.session_state.codey.load_model()
                        st.session_state.generated_code = st.session_state.codey.generate_code(st.session_state.code_prompt, code_language)
                else:
                    st.toast("Please select a valid AI option selected '{st.session_state.ai_option}' option", icon="❌")
                    st.session_state.generated_code = ""
                    logger.error(f"Please select a valid AI option selected '{st.session_state.ai_option}' option")

        # Run Code button in the fourth column
        with run_code_col:
            run_submitted = st.form_submit_button("Execute Code")
            if run_submitted:
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
            theme = st.selectbox("Theme", options=themes, index=themes.index("monokai"))

            # Keybinding setting
            keybindings = ["emacs", "sublime", "vim", "vscode"]
            keybinding = st.selectbox("Keybinding", options=keybindings, index=keybindings.index("emacs"))

            # Other settings
            show_gutter = st.checkbox("Line Number", value=True)
            show_print_margin = st.checkbox("Print Margin", value=True)
            wrap = st.checkbox("Wrap", value=True)
            auto_update = st.checkbox("Auto Update", value=False)
            readonly = st.checkbox("Readonly", value=True)
            language = st.selectbox("Language", options=list(LangCodes().keys()), index=list(LangCodes().keys()).index("Python"))
            
        # Display the st_ace code editor with the selected settings
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

    # Expander for coding guidelines
    with st.sidebar.expander("Coding Guidelines"):
        st.session_state["coding_guidelines"]["modular_code"] = st.checkbox("Modular Code")
        st.session_state["coding_guidelines"]["exception_handling"] = st.checkbox("Add Exception handling")
        st.session_state["coding_guidelines"]["error_handling"] = st.checkbox("Add Error handling")
        st.session_state["coding_guidelines"]["logs"] = st.checkbox("Add Logs")
        st.session_state["coding_guidelines"]["comments"] = st.checkbox("Add comments")
        st.session_state["coding_guidelines"]["efficient_code"] = st.checkbox("Write Efficient code")
        st.session_state["coding_guidelines"]["robust_code"] = st.checkbox("Write Robust Code")
        st.session_state["coding_guidelines"]["memory_efficiency"] = st.checkbox("Ensure memory efficiency")
        st.session_state["coding_guidelines"]["speed_efficiency"] = st.checkbox("Ensure speed efficiency")
        st.session_state["coding_guidelines"]["naming_conventions"] = st.checkbox("Standard Naming conventions")
    
def save_uploaded_file(uploadedfile):
    try:
        # Check if tempDir exists, if not, create it
        if not os.path.exists("tempDir"):
            os.makedirs("tempDir")

        with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())
        return os.path.join("tempDir", uploadedfile.name)
    except Exception as e:
        st.toast(f"Error saving uploaded file: {e}", icon="❌")
        return None

if __name__ == "__main__":
    main()
