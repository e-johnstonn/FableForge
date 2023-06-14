import os
import uuid

import deeplake

dataset_path = os.getenv('DATASET_PATH')

os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')

class SaveToDeepLake:
    def __init__(self, buildbook_instance, name=None, dataset_path=dataset_path):
        self.dataset_path = dataset_path
        try:
            self.ds = deeplake.load(dataset_path, read_only=False)
            self.loaded = True
        except:
            self.ds = deeplake.empty(dataset_path)
            self.loaded = False

        self.prompt_list = buildbook_instance.prompts_list
        self.images = buildbook_instance.source_files

        if name is None:
            self.name = str(uuid.uuid4())
        else:
            self.name = name

    def fill_dataset(self):
        if not self.loaded:
            self.ds.create_tensor('prompts', htype='text')
            self.ds.create_tensor('images', htype='image', sample_compression='png')
        for i, prompt in enumerate(self.prompt_list):
            print(i)
            self.ds.append({'prompts': prompt, 'images': deeplake.read(self.images[i])})


class TestingClass:
    def __init__(self):
        self.prompts_list = ['ksg', 'Prompt 4122', 'Prompt 214123']
        self.source_files = ['ksg.png', '2.png', '3.png']




