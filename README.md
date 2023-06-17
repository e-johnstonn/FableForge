#  📚 FableForge 

## 📄 Description

Generate a picture book from a single prompt using [OpenAI's new function calling](https://openai.com/blog/function-calling-and-other-api-updates) and [Replicate's API](https://replicate.com/) for Stable Diffusion. Store all your generated images and corresponding prompts in [Deep Lake](https://www.activeloop.ai/). Check `example.pdf` or watch the video below for a peek at the output. 

## :tv: Demo
https://github.com/e-johnstonn/FableForge/assets/30129211/9657b0de-ac80-46d1-bc30-34759b601498

## 🛠 Install
1. Clone the repository
2. Install requirements.txt
3. Set up your OpenAI and Replicate API keys in `keys.env`
4. To save your images and prompts, set up your Activeloop Deep Lake token and dataset path in `keys.env`
5. Run `streamlit run main.py` to start the app!

## Improvements
- This demo is currently set up to use the Replicate API for image generation. However, for best results, connect it to your own Stable Diffusion setup (local or cloud-based) with a custom model/LoRA specific to your use case. 

## License
[MIT License](LICENSE)





