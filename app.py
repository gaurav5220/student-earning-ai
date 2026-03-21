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
        Give 3 detailed side-income ideas.

        Budget: ₹{budget}
        Time: {time} hrs/day

        Explain each idea with:
        - What
        - How to start
        - Earnings
        - Tips
        """

        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )

        result = chat.choices[0].message.content

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)