import logging
import pprint
import os
import google.generativeai as palm
from dotenv import load_dotenv
# Set up logging
logging.basicConfig(filename='palm-coder.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PalmAI:
    def __init__(self, model="models/text-bison-001", temperature=0.3, max_output_tokens=2048, mode="balanced"):
        """
        Initialize the PalmAI class with the given parameters.
        """
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.mode = mode
        self.api_key = None
        self._configure_api()

    def _configure_api(self):
        """
        Configure the palm API with the API key from the environment.
        """
        try:
            load_dotenv()
            self.api_key = os.getenv('PALMAI_API_KEY')
            palm.configure(api_key=self.api_key)
            logger.info("Palm API configured successfully.")
        except Exception as e:
            logger.error(f"Error occurred while configuring Palm API: {e}")

    def generate_code(self, prompt):
        """
        Function to generate text using the palm API.
        """
        try:
            # Define top_k and top_p based on the mode
            if self.mode == "precise":
                top_k = 40
                top_p = 0.95
                self.temprature = 0
            elif self.mode == "balanced":
                top_k = 20
                top_p = 0.85
                self.temprature = 0.3
            elif self.mode == "creative":
                top_k = 10
                top_p = 0.75
                self.temprature = 1
            else:
                raise ValueError("Invalid mode. Choose from 'precise', 'balanced', 'creative'.")

            logger.info(f"Generating text with mode: {self.mode}, top_k: {top_k}, top_p: {top_p}")

            completion = palm.generate_text(
                model=self.model,
                prompt=prompt,
                candidate_count=4,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                top_k=top_k,
                top_p=top_p,
                stop_sequences=[],
                safety_settings=[{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
            )
            logger.info("Text generation completed successfully.")
            return completion.result
        except Exception as e:
            logger.error(f"Error occurred while generating text: {e}")
            return None

