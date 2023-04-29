import openai

openai.api_key = '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'

# text = 'Say this is a test'
# response = openai.Completion.create(
#     model="gpt-3.5-turbo", 
#     prompt=text, 
#     temperature=0, 
#     max_tokens=7)
# print(response['choices'][0]['text'])

# import os
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.Model.list())