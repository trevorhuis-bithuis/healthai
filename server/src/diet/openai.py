import openai
import re, os

# Set up OpenAI API key and model
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

    return recipe
