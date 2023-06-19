#  📚 FableForge 

## 📄 Description

Generate a picture book from a single prompt using [OpenAI's new function calling](https://openai.com/blog/function-calling-and-other-api-updates) and [Replicate's API](https://replicate.com/) for Stable Diffusion. Store all your generated images and corresponding prompts in [Deep Lake](https://www.activeloop.ai/). Check `example.pdf` or watch the video below for a peek at the output. 

Built with [LangChain](https://github.com/hwchase17/langchain), [Deep Lake](https://www.deeplake.ai/), and [Replicate](https://replicate.com/).

## :tv: Demo


https://github.com/e-johnstonn/FableForge/assets/30129211/f9523905-342e-4a33-914d-acd13bd168ec


## 🛠 Install
1. Clone the repository
2. Install requirements.txt
3. Set up your OpenAI and Replicate API keys in `keys.env` - More on this below
4. To save your images and prompts, set up your Activeloop Deep Lake token and dataset path in `keys.env` - More on this below
5. Run `streamlit run main.py` to start the app!


## 🧠 Deep Lake Setup
During the creation of this project, I used Deep Lake to store the generated pictures and prompts in the cloud, as it makes it easy to work with multiple modalities of data (image/text), and displays them in a web UI. To set this up yourself, go to the [Deep Lake website](https://www.activeloop.ai/) and make an account. Once logged in, you can click "Train deep learning models", then "Create dataset", which will guide you through getting an API token and dataset link. Put the token and dataset path in the `keys.env` file and you're good to go.

## 🖼️ Replicate Setup
A Replicate API key is necessary for this app. To get one, go to the [Replicate website](https://replicate.com/) and create an account, then take your API key and put it in `keys.env`. Replicate provides free image generation for new users. 

## 📐Architecture

![architecture](https://github.com/e-johnstonn/FableForge/assets/30129211/54dbaa98-5a89-4af4-8ff2-9640a40e773c)


## Improvements
- This demo uses Replicate for image generation due to its ease of use. Connect it to your own Stable Diffusion setup (local or cloud-based) for better results. I recommend some combination of [Diffusers](https://github.com/huggingface/diffusers) and [FastAPI](https://github.com/tiangolo/fastapi) as a starting point.


## License
[MIT License](LICENSE)





