import openai
from server import *
import pdb
import re
import requests
from bs4 import BeautifulSoup

# Prompt Goals
# - Determine if a recipe is present on the page?
# - Extract the recipe
# - Extract the number of servings
# - Extract the instructions
# - Extract the recipe title
# - Extract nutritional information
# - Extract summary of blog post? or dietary restrictions
# - site the website

test_url = 'https://www.foodnetwork.com/recipes/rachael-ray/meatloaf-muffins-with-barbecue-sauce-recipe-2118102'


def create_prompt(site_text):
    prompt = """Determine if a recipe is contained in the text and if there is a recipe, follow these instructions:
    Extract the recipe title.
    Extract the Ingredients and portions of each.
    Extract the instructions.
    Extract the number of servings.
    Extract the time it will take to make if mentioned.
    Extract the time it will take to cook if mentioned.
    Store this information in json.

    Output the result in this format:  
    {
        'recipes': [
            {'name': 'recipe name goes here', 
             'ingredients' : [
                "amount - ingredient",
                "amount - ingredient"
                ],
             'instructions' : [
             "Instruction goes here",
             "Instruction goes here"
                ],
             'serving size': 'number of servings goes here',
             'citation' : 'citation goes here'
        ]
    }


    '"""


def gpt_request(prompt):
    openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system',
                'content': 'Your job is to extract useful information from text'},
            {'role': 'user', 'content': prompt}
        ]
    )


def call_whisper():
    file = open("/path/to/file/openai.mp3", "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)
    return transcription


def get_html_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return


def get_text_from_url(soup):
    text = soup.get_text()
    return text


def get_html_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define a list of keywords to search for within the text
    keywords = ['Ingredients', 'Preparation', 'Cooking time', 'Serving size']

    # Search for all <div> tags on the page
    divs = soup.find_all('div')

    # Create a dictionary to store the score for each <div> tag
    scores = {}

    # Loop through each <div> tag and calculate its score
    for div in divs:
        # Check if the <div> tag is a child of <nav>, <menu>, or <footer>
        if div.parent.name in ['nav', 'menu', 'footer']:
            continue
        # Otherwise, calculate the score as before
        text = div.text
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        scores[div] = score

    # Find the <div> tag with the highest score
    highest_score = max(scores.values())
    highest_div = None
    for div, score in scores.items():
        if score == highest_score:
            highest_div = div
            break

    # Extract the text from the <div> tag with the highest score
    recipe_text = highest_div.text.strip()

    # Search for the keywords 'ingredients' and 'instructions' and the occurrence of at least 5 numbers
    match = re.search(r'(ingredients|instructions).*?\d.*?©',
                      recipe_text, flags=re.IGNORECASE | re.DOTALL)

    if match:
        # Get the index of the © symbol
        index = match.start(0) + match.group(0).rindex('©')
        # Extract the text before the © symbol
        result = text[:index]
        print(len(result))
        print(result)
    else:
        print("Text not found")

    print()
    return recipe_text
