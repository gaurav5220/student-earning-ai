from flask import Flask, render_template, request
import os
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
"""

        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-20b"
        )

        result = chat.choices[0].message.content

    return render_template("index.html", result=result)


if __name__ == "__main__":
   app.run(port=8080)