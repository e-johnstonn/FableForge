import re

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import replicate


from prompts import *

import requests

import streamlit as st


class BuildBook:
    sd_llm_prompt = SD_PROMPTS_PROMPT
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
        self.sd_prompts = self.get_prompts()

        self.pages_list = self.get_list_from_text(self.book_text)
        self.prompts_list = self.get_list_from_text(self.sd_prompts)
        self.prompts_list = [f'{prompt}, completely in the style of {self.style}'.strip().replace('\n', '') for prompt in self.prompts_list]

        self.source_files = self.download_images()
        self.list_of_tuples = self.create_list_of_tuples()
        self.progress.progress(1.0, "Done! Wait one moment while your book is processed...")



    def get_pages(self):
        pages = self.chat([HumanMessage(content=f'{self.book_text_prompt} Topic: {self.input_text}')]).content
        return pages

    def get_prompts(self):
        prompts = self.chat([HumanMessage(content=f'{self.sd_llm_prompt} --- Book: {self.book_text} --- Remember to generate scenery, no plot/characters'
                                                  f'Generated prompts in the style of {self.style}: ')]).content
        return prompts

    def get_list_from_text(self, text):
        new_list = re.split('Page \d+:', text)
        new_list.pop(0)
        return new_list

    def create_images(self):
        if len(self.pages_list) == len(self.prompts_list):
            image_urls = []
            for i in range(len(self.prompts_list)): # temp limit
                print(f'{self.prompts_list[i]} is the prompt for page {i+1}')
                output = replicate.run(
                    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                    input={"prompt": self.prompts_list[i],
                           "negative_prompt": "photorealistic, photograph, boring, bad anatomy, blurry, pixelated, obscure, unnatural colors, poor lighting, dull, unclear, gross,"
                                              "disfigured, wrong anatomy, weird eyes, creepy, disgusting, text, words, letters,"
                                              "photo, RAW image"},
                )
                image_urls.append(output[0])
                self.progress_steps += 1
                self.progress.progress(self.progress_steps / self.total_progress_steps, f"Generating image {i+1}...")
            return image_urls
        else:
            print(len(self.pages_list))
            print(len(self.prompts_list))
            print(self.pages_list)
            print(self.prompts_list)
            raise 'Pages and Prompts do not match'

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



