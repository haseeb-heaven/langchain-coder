# LangChain Coder AI README

## 📌 Table of Contents
1. [Introduction](#introduction)
2. [AI Sections](#ai-sections)
3. [Features](#features)
4. [WebUI - Application Showcase](#webui---application-showcase)
5. [Vertex AI Integration](#vertex-ai-integration)
6. [📸 Image Showcase](#📸-image-showcase)
7. [Packages Used](#packages-used)
8. [📚 Links and References](#📚-links-and-references)
9. [Versioning](#versioning)
10. [Contributing](#contributing)
11. [License](#license)
12. [Author](#author)

## Introduction

LangChain Coder AI is a state-of-the-art code generation tool powered by OpenAI and Vertex AI. It provides a seamless experience for developers to generate code snippets in various languages based on the provided prompts. </br>The tool is integrated with advanced AI models like </br>_**OpenAI:** GPT-3.5, GPT-3.5 Turbo, GPT-4_</br> **Google:** _Code Gecko, and Code Bison, PALM and Gemini_</br> 
Ensuring high-quality code outputs from these powerful models.

## Features

- **AI-Powered Code Generation and Completion**: Utilizes OpenAI and Vertex AI models for efficient and accurate code suggestions.
- **Save and Execute Code**: Provides options to save the generated code and execute it instantly.
- **Coding Guidelines**: Ensures the generated code adheres to standards like modularity, exception handling, error handling, logging, comments, efficiency, robustness, memory management, speed optimization, and naming conventions.
- **Advanced Code Editor**: Customize your coding experience with features like adjustable font size, tab size, themes, keybindings, line numbers, print margins, wrapping, auto-updates, read-only mode, and language selection.
- **Customizable Settings**: Adjust settings like temperature, max tokens, model name, project, region, and credentials file for Vertex AI.
- **Offline and Online Compilation Modes**: Choose between offline and online compiler modes for code execution.

## LangChain Coder in Action

[![LangChain Coder in Action](https://img.youtube.com/vi/ezlYpv_gpck/0.jpg)](https://www.youtube.com/watch?v=ezlYpv_gpck)

Watch LangChain Coder in action in this video!


## AI-Sections.
### 🤖 OpenAI 
- **Customizable Settings**: Adjust Tokens, Temperature, and set your API Key directly in the settings.
- **Model Selection**: Choose from a variety of models including GPT 3.5, GPT 3.5 Turbo, and the latest GPT 4.

### 🌐 Vertex AI 
- **Customizable Settings**: Fine-tune Tokens, Temperature, and set your Credentials Key in the settings.
- **Model Selection**: Opt for models like **Code Gecko** for completions and **Code Bison** for code generation. These models are designed to support code completion and generation, enhancing your coding experience.


## WebUI - Application Showcase

🌆 This is the main screen of the application. Dive in with a text prompt, choose your language, and let the magic happen with buttons that feel just right.</br>
![langchain-main-screen-ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/langchain-main-screen-ui.png?raw=true "")

🎨 Behold the canvas after the masterpiece is painted. Code generation was never this beautiful.</br>
![generated_code_ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/langchain-code-ui.png?raw=true "")

## OpenAI Integration
LangChain Coder AI integrates with [OpenAI](https://openai.com/) to leverage its powerful machine learning models for code generation. OpenAI is an AI research and deployment company For more details on how LangChain integrates with OpenAI, refer to the [official documentation](https://python.langchain.com/docs/integrations/providers/openai).

You need Open AI API **Key** to use LangChain Coder AI. To get your key, follow these steps:
### Get OpenAI API key

1. Go to the [OpenAI website](https://beta.openai.com/signup/).
2. Fill out the form with your information and click “Create Account”.
3. Once you are logged in, click on “API Keys” in the left-hand menu.
4. Click on “Generate New Key” to create a new API key.
5. Copy your API key – we will use it later in our Python code.

## Vertex AI Integration

LangChain Coder AI integrates with [Google Vertex AI](https://cloud.google.com/python/docs/reference/aiplatform/latest) to leverage its powerful machine learning models for code generation. Vertex AI offers a range of tools and services for ML and AI, and LangChain Coder AI taps into these resources to provide top-notch code suggestions. For more details on how LangChain integrates with Vertex AI, refer to the [official documentation](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm).

Additionally, the Vertex AI SDK for Python allows for automation of data ingestion, model training, and predictions on Vertex AI. It provides a programmatic way to access most of the functionalities available in the Google Cloud console. For more information, check out the [Vertex AI SDK for Python](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk).

You need Google Vertex **Service Account Credentials** to use LangChain Coder AI. To get your credentials, follow these steps:

### Credentials for Google Vertex AI Service account

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Click the **Menu** button (three horizontal lines) in the top left corner of the page.
3. Select **IAM & Admin** > **Service accounts**.
4. Click the **Create Service Account** button.
5. In the **Service account name** field, enter a name for your service account.
6. Select the **Editor** role for the service account.
7. Click the **Create** button.
8. Click the **Keys** tab.
9. Click the **Add Key** button.
10. Select **JSON** as the key type.
11. Click the **Create** button.

After downloading the file in `JSON` format you need to upload it in the application. To do so, follow these steps:
Enter the project name and location of that project and you're all set to go.

Here is sample Service JSON file.
```json
{
  "type": "service_account",
  "project_id": "my-project-id",
  "private_key_id": "my-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nmy-private-key\n-----END PRIVATE KEY-----\n",
  "client_email": "my-service-account@my-project-id.iam.gserviceaccount.com",
  "client_id": "my-client-id"
}
```

## PALM AI Integration:
LangChain Coder AI integrates with [PALM AI](https://ai.google/discover/palm2/) to leverage its powerful machine learning models for code generation.
- PALM AI is legacy model from Google AI and **deprecated** now.

## Gemini AI Integration:
LangChain Coder AI integrates with [GEMINI AI](https://deepmind.google/technologies/gemini/) to leverage its powerful machine learning models for code generation.
- Gemini AI is the **latest model** from Google AI and successor of PALM AI.

### Setup: Get PALM/GEMINI AI key

*Step 1:* **Obtain the Google Palm/Gemini API key.**.</br>
*Step 2:* Visit the following URL: *https://makersuite.google.com/app/apikey*.</br>
*Step 3:* Click on the **Create API Key** button.</br>
*Step 4:* The generated key is your API key. </br>Please make sure to **copy** it and **paste** it in the required field below.</br>
*Note:* The API key is crucial for the functioning of Google AI models. Please ensure to keep it safe and do not share it with anyone.</br>

## 📸 Image Showcase
**__Main Screen UI__**  
*The main screen of the application.*  
![langchain-main-screen-ui](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-main-screen-ui.png?raw=true "")  
</br>

**__Generated Code UI__**  
*Displays the generated code in a user-friendly UI.*  
![generated_code_ui](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-ui.png?raw=true "")  
</br>

**__API Rates__**  
*Shows the API rates for OpenAi and Vertex AI.*  
![langchain-api-rates](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-api-rates.png?raw=true "")  
</br>

**__Dark Theme Code Editor__**  
*A dark-themed code editor for a comfortable coding experience.*  
![langchain-code-editor-dark-theme](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-editor-dark-theme.png?raw=true "")  
</br>

**__Coding Guidelines__**  
*Highlights the coding guidelines supported by LangChain Coder AI.*  
![langchain-code-guidelines](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-guidelines.png?raw=true "")  
</br>

**__Offline Compiler__**  
*Showcases the offline compiler mode for executing code.*  
![langchain-offline-compiler](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-offline-compiler.png?raw=true "")  
</br>

**__Online Compiler__**  
*The online compiler mode with support for multiple languages.*  
![langchain-online-compiler](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-online-compiler.png?raw=true "")  
</br>

**__Swift Code Demo__**  
*A demonstration showcasing Swift code generation.*  
![langchain-swift-code-demo](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-swift-code-demo.png?raw=true "")  
</br>

**__Vertex AI Code Gecko__**  
*Illustrates the code completion feature of Vertex AI Code Gecko.* 
![langchain-vertex-ai-code-gecko](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-vertex-ai-code-gecko.png?raw=true "")  
</br>




## Packages Used

- **streamlit**: A fast and simple way to create data apps.
- **streamlit_ace**: A Streamlit component for the Ace editor.
- **google-auth**: A Google Authentication Library.
- **google-auth-oauthlib**: A Google Authentication Library for OAuth.
- **google-cloud-aiplatform**: A client library for interacting with the Vertex AI API.
- **langchain**: A Python client library for interacting with the LangChain API.
- **openai**: A Python client library for interacting with the OpenAI API.
- **python-dotenv**: Reads the key-value pair from .env file and adds them to environment variable.
- **vertexai**: A Python client library for interacting with the Vertex AI API.


## 📚 Links-and-References
- [Google Vertex AI Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [LangChain Integration with Vertex AI](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm)
- [Vertex AI SDK for Python](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)


## Versioning

**Version 1.5** includes these features:
- **GEMINI AI Integration**: LangChain Coder AI integrates with GEMINI AI.
- **Customizable Settings**: Adjust Tokens, Temperature, and set your API Key directly in the settings.
- **Model Selection**: Choose from a variety of models including **gemini-pro**,**emini-pro-vision**.
- **GEMINI AI Models** GEMINI 2 Supports the following models:
  - **gemini-pro**: A chatbot model that can be used to generate responses to a given prompt.
  - **gemini-pro-vision**: An image generation model that can be used to generate text from a given prompt


**Version 1.4** includes these features:
- **PALM AI Integration**: LangChain Coder AI integrates with PALM AI.
- **Customizable Settings**: Adjust Tokens, Temperature, and set your API Key directly in the settings.
- **Model Selection**: Choose from a variety of models including **chat-bison**,**text-bison**,**embedding-gecko**.
- **PALM AI Models** PALM 2 Supports the following models:
  - **chat-bison**: A chatbot model that can be used to generate responses to a given prompt.
  - **text-bison**: A text generation model that can be used to generate text from a given prompt.
  - **embedding-gecko**: A text embedding model that can be used to generate embeddings for a given text.

**Version 1.3** includes these features:

- *AI-powered code generation and completion*
- *Uses OpenAI and Vertex AI models*
- *Save, execute code, and select coding guidelines*
- *Advanced code editor features*
- *Customizable Vertex AI settings*
- *Offline and online compilation modes*
- *Coding guidelines*: 
  - *Modularity*
  - *Exception handling*
  - *Error handling*
  - *Logging*
  - *Comments*
  - *Efficiency*
  - *Robustness*
  - *Memory management*
  - *Speed optimization*
  - *Naming conventions*

**New in version 1.3:** AI-powered code generation and completion using OpenAI and Vertex AI models.

## Contributing
If you want to contribute to this project and make it better with new ideas, your pull request is very welcomed. If you find any issue just put it in the repository issue section, thank you.

## License
This project is licensed under the MIT License so feel free to use it.

## Author
Crafted with ❤️ by HeavenHM.
