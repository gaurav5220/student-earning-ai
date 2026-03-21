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
Give 3 realistic side-income ideas for an Indian college student.

Budget: ₹{budget}
Time available: {time} hours/day

For EACH idea, give FULL detailed explanation in this format:

1. Idea Name

- What is it (2-3 lines explanation)
- Why it works (clear reasoning)
- How to start (step-by-step)
- Required skills
- Investment needed
- Expected monthly earning (realistic ₹ range)
- Platforms to use (real apps/websites)
- Pro tips to succeed

Make it practical, beginner-friendly, and detailed.
Do NOT keep it short.
"""

        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-20b"
        )

        result = chat.choices[0].message.content

    return render_template("index.html", result=result)


if __name__ == "__main__":
 import os

if __name__ == "__main__":
    app.run(debug=True)