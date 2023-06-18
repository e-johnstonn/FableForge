BOOK_TEXT_PROMPT = """
Write a 3-6 page children's picture book. Each page should have 2-3 sentences. It should be rhyming.
We will be adding pictures of the environment/scenery for each page, so pick a pretty setting/place. Limit of 7 pages,
do not exceed 3 sentences per page. Do not exceed 7 pages.

Before the story begins, write a "Page 0: {title}" page. The title should be the name of the book, no more than four words.


Format like: Page 0: {title}, Page 1: {text}, etc. Do not write anything else. 
"""


get_visual_description_function = [{
    'name': 'get_passage_setting',
    'description': 'Generate and describe the visuals of a passage in a book. Visuals only, no characters, plot, or people.',
    'parameters': {
        'type': 'object',
        'properties': {
            'setting': {
                'type': 'string',
                'description': 'The visual setting of the passage, e.g. a green forest',
            },
            'time_of_day': {
                'type': 'string',
                'description': 'The time of day of the passage, e.g. nighttime, daytime. If unknown, leave blank.',
            },
            'weather': {
                'type': 'string',
                'description': 'The weather of the passage, eg. rain. If unknown, leave blank.',
            },
            'key_elements': {
                'type': 'string',
                'description': 'The key visual elements of the passage, eg tall trees',
            },
            'specific_details': {
                'type': 'string',
                'description': 'The specific visual details of the passage, eg moonlight',
            }
        },
        'required': ['setting', 'time_of_day', 'weather', 'key_elements', 'specific_details']
    }
}]

get_lighting_and_atmosphere_function = [{
    'name': 'get_lighting_and_atmosphere',
    'description': 'Generate a visual description of the overall atmosphere and color palette of a book',
    'parameters': {
        'type': 'object',
        'properties': {
            'base_setting': {
                'type': 'string',
                'description': 'The base setting of the book, eg. ancient Rome, a forest in Washington, space',
            },
            'lighting': {
                'type': 'string',
                'description': 'The lighting atmosphere of the book, eg. cheerful atmosphere',
            },
            'mood': {
                'type': 'string',
                'description': 'The mood of the book, eg. lively mood',
            },
            'color_palette': {
                'type': 'string',
                'description': 'The color palette of the book, eg. bright and vivid color palette',
            },
        },
        'required': ['base_setting', 'lighting', 'mood', 'color_palette']
    }
}]
