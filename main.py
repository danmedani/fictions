import openai
from typing import List
from typing import Dict
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--api-key', required=True, help='API key for Open AI')
    parser.add_argument('--gpt4', action='store_true', help='Use the wicked smaht GPT4 model')
    return parser.parse_args()

def create_chat_completion(messages, model=None, temperature=None) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

def get_novelist_prompt(novel_idea: str) -> str:
    with open('prompts/novelist_prompt.txt', 'r') as f:
        return f.read().format(novel_idea=novel_idea)

def get_critic_prompt() -> str:
    with open('prompts/critic_prompt.txt', 'r') as f:
        return f.read()

def get_editor_prompt(feedback: str) -> str:
    with open('prompts/editor_prompt.txt', 'r') as novelist_prompt_file:
        return novelist_prompt_file.read().format(feedback=feedback)

def get_novelist_messages(novel: str, novel_idea: str) -> List[Dict]:
    return [
        {
            'role': 'system',
            'content': get_novelist_prompt(novel_idea=novel_idea)
        },
        {
            'role': 'user',
            'content': novel
        }
    ]

def get_critic_messages(novel: str) -> List[Dict]:
    return [
        {
            'role': 'system',
            'content': get_critic_prompt()
        },
        {
            'role': 'user',
            'content': novel
        }
    ]


def get_editor_messages(novel: str, feedback: str) -> List[Dict]:
    return [
        {
            'role': 'system',
            'content': get_editor_prompt(feedback=feedback)
        },
        {
            'role': 'user',
            'content': novel
        }
    ]


args = parse_arguments()
openai.api_key = args.api_key

print("""
Welcome to novel creation bot.

""")
novel_idea: str = input("This story is about: ")

novel = 'Chapter 1\n'
while True:
    next_sentence = create_chat_completion(
        messages=get_novelist_messages(novel, novel_idea),
        model='gpt-4' if args.gpt4 else "gpt-3.5-turbo",
        temperature=0.6
    )
    print('\nNOVELIST\n {}'.format(next_sentence))

    tmp_novel = novel + next_sentence
    critic_feedback = create_chat_completion(
        messages=get_critic_messages(tmp_novel),
        model='gpt-4' if args.gpt4 else "gpt-3.5-turbo",
        temperature=0.5
    )
    print('\nCRITIC\n {}'.format(critic_feedback))
    editor_text = create_chat_completion(
        messages=get_editor_messages(tmp_novel, critic_feedback),
        model='gpt-4' if args.gpt4 else "gpt-3.5-turbo",
        temperature=0.5
    )

    print('\nEDITOR\n {}'.format(editor_text))
    novel = editor_text
