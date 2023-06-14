BOOK_TEXT_PROMPT = """
Write a 3-6 page children's picture book. Each page should have 2-3 sentences. It should be rhyming.
We will be adding pictures of the environment/scenery for each page, so pick a pretty setting/place. Limit of 7 pages,
do not exceed 3 sentences per page. DO NOT EXCEED 7 PAGES.

Before the story begins, write a "Page 0: title" page. The title should be the name of the book, no more than four words.


Format like: Page 0: title, Page 1: text, etc.
"""

SD_PROMPTS_PROMPT = """
Create distinct Stable Diffusion (SD, image generator) prompts for each page of a children's book, focusing solely on the environmental visuals. 
Each prompt must depict every detail of the scene, from time of day to the setting's nature.

Ensure all prompts maintain a consistent artistic style - vibrant, playful, and child-friendly.

SD cannot recall previous prompts or identify characters or the story. 
Therefore, avoid referencing plot details, character names, or any story-specific elements.

Each prompt must stand alone, providing a comprehensive description of the unique scene. 
Don't include characters or plot, only the environment. Abstract descriptions are acceptable, provided there's a clear continuity between prompts.

Remember - each prompt should solely describe the visual scene, and should never reference other prompts or the storyline itself. 
The aim is to illustrate the environmental scenery, not the plot or characters.

Prompt template for you to fill in:

{Setting}, {Time of Day}, {Weather/Climate}, {Key Elements}, {*Color Palette*}, {*Lighting Atmosphere*}, {Specific Details}

Example page: In the forest at night, the trees stand tall and still. The animals are tucked in, cozy and chill.
Example prompt: green forest, night, moonlight, tall trees, dark color palette, mysterious atmosphere, eerie mood

Example page: The sun is shining, the sky is blue. The birds are singing, the flowers are too. Ted waddled over to the bench and sat down.
Example prompt: beautiful field, daytime, sunny and clear, bright flowers, bright and vivid color palette, cheerful atmosphere, lively mood

Format for you to follow: Page 0: Prompt, Page 1: Prompt, etc.

Page 0 should just be a pretty picture inspired by the scenery of the book. Ensure every prompt is related to the book's scenery.
Do not mention characters or plot.


Childrens book: 

"""