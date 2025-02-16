import configparser
import google.generativeai as genai
config = configparser.ConfigParser()
config.read('config.ini')

gemini_api_key = config['GEMINI']['api_key']
genai.configure(api_key=gemini_api_key)

class Gemini:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.max_output=8000
        self.temperature=0.2
    
    def get_text_response(self, prompt):
        generation_config=genai.types.GenerationConfig(max_output_tokens=self.max_output,temperature=self.temperature)
        response = self.model.generate_content([prompt],generation_config=generation_config)
        return response.text
