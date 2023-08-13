from os import getenv
from pathlib import Path

import openai

from publish.files import read_file, write_file
from publish.text import include_files
from writer.pub_script import pub_path, pub_url


def transform_prompt(prompt):
    openai.api_key = getenv("OPENAI_API_KEY")

    # Try up to ten times to transfer
    for i in range(10):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=3000)

        message = response['choices'][0]['message']['content']
        prompt.append({"role": "assistant", "content": message})

        finish_reason = response['choices'][0]['finish_reason']
        if finish_reason != 'length':
            return '\n\n'.join([m['content'] for m in prompt if m['role'] == 'assistant'])

    # Return the failed conversation
    return '\n\n'.join([m['content'] for m in prompt if m['role'] == 'assistant'])


def read_prompt_file(doc_file):

    def ai_prompt(prompt, system_prompt):
        state = [
            dict(role='user', content=prompt)
        ]
        if system_prompt:
            state.append(dict(role='system', content=system_prompt))
        return state

    prompt_file = str(doc_file).replace('.md', '.ai')
    prompt = include_files(read_file(prompt_file), doc_file.parent)
    system_prompt = include_files('[[System.ai]]', doc_file.parent)
    return ai_prompt(prompt, system_prompt)


def update_with_ai(doc_file):
    prompt_file = str(doc_file).replace('.md', '.ai')
    prompt = include_files(read_file(prompt_file), doc_file.parent)
    prompt = read_prompt_file(doc_file)
    text = transform_prompt(prompt)
    write_file(doc_file, text, overwrite=True)


def pub_ai(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    doc_file = pub_path(pub, chapter, doc)
    update_with_ai(doc_file)

    url = pub_url(pub, chapter, doc)
    return url
