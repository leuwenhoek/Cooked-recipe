from flask import Flask, render_template, redirect, request, jsonify, url_for
import google.generativeai as genai
from dotenv import load_dotenv
import os
import markdown 
from urllib.parse import quote_plus

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def redirection():
    return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        food = (data.get('request') or '').strip()
        if not food:
            return jsonify({"status": "error", "message": "Empty request"}), 400

        redirect_url = url_for('recipe_page', food=food)
        return jsonify({"status": "success", "redirect_url": redirect_url})

    return render_template('home.html')


def generate_recipe(food: str) -> str:
    prompt = (
        f"You are a GenZ bestie roasting the user while writing a recipe for {food}. "
        "Rules for your response:\n"
        "1. Start by roasting the user's relationship status or their life choices based on this food choice. "
        "(e.g., if they ask for Ramen, roast them for being broke or single).\n"
        "2. Use GenZ slang (no cap, bet, lowkey, mid, bruh, main character energy, delulu).\n"
        "3. Format the recipe clearly with a Title, Prep Time, Ingredients, and Instructions.\n"
        "4. Use emojis and memes in text form (e.g., 👁️👄👁️, 💀, 🚩).\n"
        "5. Keep it under 1000 words but provide the actual full cooking method.\n"
        "6. Be personal—act like you've known them for years and you're tired of their 'situationship' drama."
    )
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=4000  
            )
        )
        
        if response.text:
            return markdown.markdown(response.text)
        return "Chef Bot is a bit confused. Try another dish!"

    except Exception as e:
        print(f"Generation error: {e}")
        return "The kitchen is temporarily closed. Please try again in a moment."

@app.route('/recipe')
def recipe_page():
    food = request.args.get('food', 'Your Request')
    bot_response = generate_recipe(food)
    return render_template('recipe.html', food=food, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)