import re
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import replicate

import json


from prompts import *

import requests

import streamlit as st

load_dotenv('keys.env')


class BuildBook:
    book_text_prompt = BOOK_TEXT_PROMPT

    def __init__(self, model_name, input_text, style):
        self.chat = ChatOpenAI(model_name=model_name)
        self.input_text = input_text
        self.style = style

        self.progress = st.progress(0)
        self.progress_steps = 0
        self.total_progress_steps = 30

        self.progress_steps += 2
        self.progress.progress(self.progress_steps / self.total_progress_steps, "Generating book text...")
        self.book_text = self.get_pages()

        self.progress_steps += 2
        self.progress.progress(self.progress_steps / self.total_progress_steps, "Generating SD prompts...")

        self.pages_list = self.get_list_from_text(self.book_text)

        self.sd_prompts_list = self.get_prompts()


        self.source_files = self.download_images()
        self.list_of_tuples = self.create_list_of_tuples()
        self.progress.progress(1.0, "Done! Wait one moment while your book is processed...")



    def get_pages(self):
        pages = self.chat([HumanMessage(content=f'{self.book_text_prompt} Topic: {self.input_text}')]).content
        return pages

    def get_prompts(self):
        base_atmosphere = self.chat([HumanMessage(content=f'Generate a visual description of the overall lightning/atmosphere of this book using the function.'
                                                          f'{self.book_text}')], functions=get_lighting_and_atmosphere_function)
        base_dict = func_json_to_dict(base_atmosphere)

        summary = self.chat([HumanMessage(content=f'Generate a concise summary of the setting and visual details of the book')]).content

        base_dict['summary_of_book_visuals'] = summary

        def generate_prompt(page, base_dict):
            prompt = self.chat([HumanMessage(content=f'General book info: {base_dict}. General style: {self.style} Passage: {page}.'
                                                     f' Generate a visual description of the passage using the function.'
                                                     f'Creatively fill all parameters with guessed/assumed values if they are missing.')],
                               functions=get_visual_description_function)
            return func_json_to_dict(prompt)

        with ThreadPoolExecutor(max_workers=10) as executor:
            prompt_list = list(executor.map(generate_prompt, self.pages_list, [base_dict] * len(self.pages_list)))

        prompts = prompt_combiner(prompt_list, base_dict, self.style)


        return prompts

    def get_list_from_text(self, text):
        new_list = re.split('Page \d+:', text)
        new_list.pop(0)
        return new_list

    def create_images(self):
        if len(self.pages_list) != len(self.sd_prompts_list):
            raise 'Pages and Prompts do not match'

        def generate_image(i, prompt):
            print(f'{prompt} is the prompt for page {i + 1}')
            output = replicate.run(
                "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                input={"prompt": 'art,' + prompt,
                       "negative_prompt": "photorealistic, photograph, bad anatomy, blurry, gross,"
                                          "weird eyes, creepy, text, words, letters, realistic"
                                          },
            )
            return output[0]

        with ThreadPoolExecutor(max_workers=10) as executor:
            image_urls = list(executor.map(generate_image, range(len(self.sd_prompts_list)), self.sd_prompts_list))

        return image_urls

    def download_images(self):
        image_urls = self.create_images()
        source_files = []
        for i, url in enumerate(image_urls):
            r = requests.get(url, stream=True)
            file_path = f'images/{i+1}.png'
            with open(file_path, 'wb') as file:
                source_files.append(file_path)
                for chunk in r.iter_content():
                    file.write(chunk)
                self.progress_steps += 1
                self.progress.progress(self.progress_steps / self.total_progress_steps, f"Downloading image {i+1}...")
        return source_files

    def create_list_of_tuples(self):
        files = self.source_files
        text = self.pages_list
        return list(zip(files, text))


def func_json_to_dict(response):
    return json.loads(response.additional_kwargs['function_call']['arguments'])


def prompt_combiner(prompt_list, base_dict, style):
    prompts = []
    for i, prompt in enumerate(prompt_list):
        entry = f"{prompt['base_setting']}, {prompt['setting']}, {prompt['time_of_day']}, {prompt['weather']}, {prompt['key_elements']}, {prompt['specific_details']}, " \
                f"{base_dict['lighting']}, {base_dict['mood']}, {base_dict['color_palette']}, in the style of {style}"
        prompts.append(entry)
    return prompts

def process_page(chat, page, base_dict):
    prompt = chat([HumanMessage(content=f'General book info: {base_dict}. Passage: {page}')],
                      functions=get_visual_description_function)
    return func_json_to_dict(prompt)

