from flask import Flask, render_template, request, session, Response, redirect, url_for
import os
import secrets
from datetime import datetime
from groq import Groq

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    budget = ""
    time_val = ""

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        budget = request.form.get("budget", "")
        time_val = request.form.get("time", "")

        prompt = f"""
Give 3 realistic side-income ideas for an Indian college student.

Budget: ₹{budget}
Time available: {time_val} hours/day

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

        history = session.get("history", [])
        history.insert(0, {
            "id": len(history),
            "budget": budget,
            "time": time_val,
            "result": result,
            "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        })
        session["history"] = history[:20]   # keep last 20 entries
        session.modified = True

    return render_template(
        "index.html",
        result=result,
        budget=budget,
        time_val=time_val,
        history=session.get("history", []),
    )


@app.route("/download")
def download():
    """Return the most-recent result as a plain-text file."""
    history = session.get("history", [])
    if not history:
        return redirect(url_for("index"))

    entry = history[0]
    text = (
        f"Student Side-Income Ideas\n"
        f"Generated: {entry['timestamp']}\n"
        f"Budget: ₹{entry['budget']}  |  Free time: {entry['time']} hrs/day\n"
        f"{'=' * 60}\n\n"
        f"{entry['result']}"
    )
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=side-income-ideas.txt"},
    )


@app.route("/clear-history", methods=["POST"])
def clear_history():
    session["history"] = []
    session.modified = True
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)