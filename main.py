import os

from dotenv import load_dotenv

import streamlit as st
from api_utils import BuildBook
from deep_lake_utils import SaveToDeepLake
from pdf_gen_utils import build_pdf


STYLES = {'Impressionism': 'Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light',
            'Cubism': 'Cubist art style, Picasso, fragmented forms, geometric shapes, angular lines, limited color palette, artistic',
            'Surrealism': 'Surrealist art style, dreamlike, abstract art, dream-like artwork, Salvador Dalí, art'}


load_dotenv('keys.env')

dataset_path = os.getenv('DATASET_PATH')



def main():
    st.title("Picture Book Generator")
    user_input = st.text_input("Enter a prompt to generate a picture book based off of:", max_chars=70)
    style = st.selectbox("Select a style for your picture book:", [key for key in STYLES.keys()])
    model = st.radio("Select a model to use", ['gpt-3.5-turbo', 'gpt-4'])
    # deep_lake = st.checkbox("Save to Deep Lake?")
    if 'not_saving' not in st.session_state:
        st.session_state['not_saving'] = True
    if st.button('Generate!') and user_input and st.session_state['not_saving']:
        with st.spinner('Generating your book...'):
            build_book = BuildBook(model, user_input, f'{STYLES[style]}')
            pages = build_book.list_of_tuples
            finished_pdf = build_pdf(pages, 'result.pdf')
            file_bytes = open(finished_pdf, 'rb').read()
            st.download_button(label='Download Book', data=file_bytes, file_name='picture_book.pdf',
                               key='download_button')
            st.write('Your book has been generated! Click the download button to download it. It is also saved'
                     'in the project directory.')
        # if deep_lake and st.session_state['not_saving']:
        #     st.session_state['not_saving'] = False
        #     with st.spinner('Saving to DeepLake...'):
        #         SaveToDeepLake(build_book, dataset_path=dataset_path).fill_dataset()
        #         st.write(
        #             f'Your images and SD prompts have been saved to Deep Lake! You can view it here:' + "https:/app.activeloop.ai/ethanjohnston/sd_images_and_prompts_db")
        #         st.session_state['not_saving'] = True







if __name__ == '__main__':
    main()
