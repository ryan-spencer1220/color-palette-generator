import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env");
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
  template_folder='templates'
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    You should generate color palettes that fit the the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: Beautiful Sunset
    A: ["#C34F63","#E0845E","#EEBE9F","#F4E4AA","#F7CDB0","#F2AFAC","#E68AAE","#CB6BC8"]

    Q: Convert the following verbal description of a color palette into a list of colors: Google Brand Colors
    A: ["#4285F4","#DB4437","#F4B400","#0F9D58"]

    Desired Format: JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:

    Result:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
  query = request.form.get("query")
  colors = get_colors(query)
  return {"colors": colors}

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)