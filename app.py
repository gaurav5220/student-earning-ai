from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

client = Groq(api_key="your_groq_api_key")

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        budget = request.form.get("budget")
        time = request.form.get("time")

        prompt = f"""
Suggest 3 realistic ways for a student in India to earn money.

Budget: {budget}
Time per day: {time}

Return ONLY in this format:

Idea 1:
Title:
Earning:
Difficulty:
Steps:

Idea 2:
Title:
Earning:
Difficulty:
Steps:

Idea 3:
Title:
Earning:
Difficulty:
Steps:
"""

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="groq/compound-mini"
        )

        result = chat_completion.choices[0].message.content

    return render_template("index.html", result=result)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=10000)