import openai
import re, os

openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "text-davinci-003"


def generate_recipe(ingredients, allergies):
    prompt = f"Write a recipe with {len(ingredients)} ingredients"
    if allergies:
        prompt += f" that doesn't contain {', '.join(allergies)}"
    prompt += f". The ingredients are: {', '.join(ingredients)}. You may add more ingredients except for the allergies."

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    recipe = response.choices[0].text.strip()

    # Remove any unwanted text from the recipe
    recipe = re.sub(r"^\d+\.?\s*", "", recipe, flags=re.M)
    recipe = re.sub(r"\n+", "\n", recipe)
    recipe = re.sub(r"\n\s+\n", "\n\n", recipe)

    return parse_recipe_to_object(recipe)


def parse_recipe_to_object(recipe_str):
    recipe = {"ingredients": [], "instructions": []}
    recipe_split = recipe_str.split("\n")
    recipe["title"] = recipe_split.pop(0)
    recipe_split.pop(0)  # pop the ingredients header

    for i in range(len(recipe_split)):
        if "Instructions:" in recipe_split[i]:
            recipe_split = recipe_split[i + 1 :]
            break
        recipe["ingredients"].append(recipe_split[i])

    for i in range(len(recipe_split)):
        recipe["instructions"].append(recipe_split[i])

    return recipe
