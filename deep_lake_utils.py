import os

import deeplake
from dotenv import load_dotenv

load_dotenv('keys.env')
os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')
class SaveToDeepLake:
    def __init__(self, buildbook_instance, name=None, dataset_path=None):
        self.dataset_path = dataset_path
        try:
            self.ds = deeplake.load(dataset_path, read_only=False)
            self.loaded = True
        except:
            self.ds = deeplake.empty(dataset_path)
            self.loaded = False

        self.prompt_list = buildbook_instance.sd_prompts_list
        self.images = buildbook_instance.source_files

    def fill_dataset(self):
        print('filling dataset')
        if not self.loaded:
            print('creating tensors')
            self.ds.create_tensor('prompts', htype='text')
            self.ds.create_tensor('images', htype='image', sample_compression='png')
        print('appending')
        print(self.prompt_list)
        for i, prompt in enumerate(self.prompt_list):
            print(i)
            self.ds.append({'prompts': prompt, 'images': deeplake.read(self.images[i])})



