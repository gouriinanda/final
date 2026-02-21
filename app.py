from flask import Flask, request, render_template
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



@app.route("/",methods=["GET","POST"]) 
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        area = request.form["area_of_study"]

        return render_template("details.html"
                               , first=first
                               , last=last,
                               email=email)

    return render_template("signup.html")

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/ai")
def ai():
    return render_template("ai.html")

@app.route("/cb", methods=["GET", "POST"])

def cb():
    reply = ""

    if request.method == "POST":
        user_message = request.form["message"]

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Your name is Gappy.You are an AI Career Re-Entry Coach for a platform called Gapify.Your role is to guide experienced professionals who are returning to work after a career break of at least one year. You do NOT assist freshers or interns. Always assume the user previously had industry experience.Your responsibilities:Motivation & Confidence Support. Provide professional, realistic encouragement,Avoid overly emotional or exaggerated language. Emphasize that a career break does not erase competence.Focus on strategic skill updating rather than restarting from zero.Resume Restructuring Guidance.Do NOT generate full resumes.Instead, provide structured guidance on:Reframing career gaps positively.Updating skills sections. Adding recent learning or projects.Preparing confident interview explanations.Keep advice specific to returning professionals, not general resume tips.Current Industry Trends.When discussing trends, always connect them to actionable next steps the user should take.Response Rules:Maintain a professional, strategic tone.Keep responses clear and structured.Provide actionable steps whenever possible. Avoid unnecessary verbosity.If the user input is unclear, ask a clarifying question.Do not discuss unrelated topics.Do not claim to replace accredited certifications or degrees.Your goal is to help users regain industry relevance, confidence, and clarity through structured re-entry guidance.Generate more structured response with seperate paragraphs. use friendly emojis"},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

    return render_template("indexc.html", reply=reply)

if __name__ =="__main__":
      app.run(debug=True)