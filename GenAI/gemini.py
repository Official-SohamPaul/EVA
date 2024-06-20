import google.generativeai as genai

genai.configure(api_key='AIzaSyBqmzuZXXl0FIFnL1bfZrj27nlfRG0dJAQ')

model=genai.GenerativeModel('gemini-pro')

def generate_text(query:str):
    if query is not None and query !='':
        response=model.generate_content('make a summery '+query,generation_config=genai.types.GenerationConfig(candidate_count=1,stop_sequences=None,max_output_tokens=200))
        # print(response.text)
        return response.text.replace('*','')

def generate_fullcontent(query:str):
    if query is not None:
        responses=model.generate_content(query)
        return responses
# for chunk in response:
#     print(f'{chunk.text} ')
