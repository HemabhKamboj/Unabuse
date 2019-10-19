from flask import session, request, render_template, redirect, jsonify, flash
import flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import os

from werkzeug.utils import secure_filename

app = flask.Flask(__name__)



# Check for environment variable
if not os.getenv("DATABASE_URI"):
    raise RuntimeError("DATABASE URI is not set")

app.config['DEBUG'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
MYDIR = os.path.dirname(__file__)
# Set up database
engine = create_engine(os.getenv("DATABASE_URI"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/home")
def index():
    return 'hello_world'

@app.route("/submit_form", methods = "GET")
def submit():
    if request.method=="GET":
        db.execute("INSERT INTO form_response (victim_name, reporter_name, victim_qualification, mental_state,problem_facing,duration, family_income,members,supportive ) VALUES(:victim_name, :reporter_name, :victim_qualification, :mental_state, :problem_facing,duration, :family_income, :members, :supportive)",
                   {"victim_name":request.form.get("victim_name"),
                    "reporter_name":request.form.get("reporter_name"),
                    "victim_qualification":request.form.get("victim_qualification"),
                    "mental_state":request.form.get("mental_state"),
                    "problem_facing":request.form.get("problem_facing"),
                    "duration":request.form.get("duration"),
                    "family_income":request.form.get("family_income"),
                    "members":request.form.get("members"),
                    "supportive":request.form.get("supportive")})
        db.commit()


    return 'submitted'
if __name__ == "__main__":
    main()
