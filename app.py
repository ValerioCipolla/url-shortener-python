from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import string
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Urls(db.Model):
  __tablename__ = "urls"

  id = db.Column(db.Integer, primary_key=True)
  long = db.Column(db.String())
  short = db.Column(db.String(3))
  
  def __init__(self, long, short):
    self.long = long
    self.short = short

  def __repr__(self):
    return f"long: {self.long} - short: {self.short} \n"

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.route("/", methods=["POST", "GET"])

def hello_world():
  urls = Urls.query.all()
  print(urls)
  if request.method == "POST":
    url_received = request.form["url"]
    found_url = Urls.query.filter_by(long=url_received).first()
    if found_url:
      return {
        "long_url": found_url.long,
        "short_url": found_url.short
      }
    else:
      short_url = shorten_url()
      new_url = Urls(url_received, short_url)
      db.session.add(new_url)
      db.session.commit()
      return {
        "long_url": url_received,
        "short_url": short_url
      }
  else:
      return render_template("home.html")