import os, re
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "text-davinci-003"


def generate_workout(duration, body_parts):
    prompt = f"Create a {duration} minute workout for the following body parts: {', '.join(body_parts)}"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    workout = completions.choices[0].text.strip()

    workout = re.sub(r"^\d+\.?\s*", "", workout, flags=re.M)
    workout = re.sub(r"\n+", "\n", workout)
    workout = re.sub(r"\n\s+\n", "\n\n", workout)

    return workout.split("\n")
