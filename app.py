from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)


app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    title = survey.title
    instructions = survey.instructions
    return render_template("index.html", title=title, instructions=instructions)


@app.route("/begin", methods=["GET", "POST"])
def start_survey():
    """Clear the session of responses."""

    session['responses'] = []

    return redirect("/questions/0")


@app.route('/questions/<int:qid>')
def get_questions(qid):
    title = survey.title
    responses = session.get('responses')

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f'Invalid question ID: {qid}', 'danger')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("questions.html", title=title, question=question)


@app.route('/answer', methods=["POST"])
def handle_answer():
    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")
