import os
import openai
from typing import List
from typing import Dict
import argparse

def create_completion(prompt: str, model: str, temperature: float) -> str:
    return openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature
    )

def get_novelist_prompt(novel_idea: str, story_so_far: str) -> str:
    with open('prompts/novelist_prompt.txt', 'r') as f:
        return f.read().format(novel_idea=novel_idea, story_so_far=story_so_far)

def get_slimmer_prompt(story: str) -> str:
    with open('prompts/slimmer_prompt.txt', 'r') as f:
        return f.read().format(story=story)

def get_critic_prompt(story: str) -> str:
    with open('prompts/critic_prompt.txt', 'r') as f:
        return f.read().format(story=story)

def get_editor_prompt(feedback: str, story: str) -> str:
    with open('prompts/editor_prompt.txt', 'r') as novelist_prompt_file:
        return novelist_prompt_file.read().format(feedback=feedback, story=story)

openai.api_key = os.getenv("OPENAI_API_KEY")

print("""
Welcome to novel creation bot.

""")
novel_idea: str = input("This story is about: ")
story = 'Chapter 1\n\n'
while True:
    novelist_prompt = get_novelist_prompt(novel_idea, story)
    print('\nNOVELIST PROMPT\n')
    print(novelist_prompt)
    next_paragraph = create_completion(
        model='gpt-4',
        prompt=novelist_prompt,
        temperature=0.7
    )
    print('\nNOVELIST RESPONSE\n {}'.format(next_sentence))
    story = story + next_paragraph
    # tmp_novel = novel + next_sentence
    # critic_feedback = create_completion(
    #     messages=get_critic_messages(tmp_novel),
    #     model='gpt-4' if args.gpt4 else "gpt-3.5-turbo-0301",
    #     temperature=0.7
    # )
    # print('\nCRITIC\n {}'.format(critic_feedback))
    # editor_text = create_completion(
    #     messages=get_editor_messages(tmp_novel, critic_feedback),
    #     model='gpt-4' if args.gpt4 else "gpt-3.5-turbo-0301",
    #     temperature=0.7
    # )
    # print('\nEDITOR\n {}'.format(editor_text))
    # slimmer_text = create_completion(
    #     messages=get_slimmer_messages(editor_text),
    #     model='gpt-4' if args.gpt4 else "gpt-3.5-turbo-0301",
    #     temperature=0.4
    # )

    # print('\SLIMMER\n {}'.format(slimmer_text))
    # novel = slimmer_text
