from flask import Flask, render_template, request, url_for, redirect
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
  short = db.Column(db.String())
  
  def __init__(self, long, short):
    self.long = long
    self.short = short

  def __repr__(self):
    return f"\n id: {self.id} - long: {self.long} - short: {self.short}"

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return request.base_url + rand_letters

@app.route("/", methods=["POST", "GET"])

def home_page():
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

@app.route("/all")
def show_all_urls():
  urls = Urls.query.all()
  result = {}
  for url in urls:
    result[url.id] = {"long_url": url.long, "short_url": url.short}
  return result

@app.route("/<short_url>")
def redirection(short_url):
  url = Urls.query.filter_by(short=request.base_url).first()
  if url:
    return redirect(url.long)
  else:
    return f"<h1>Url with shortcut '{short_url}' does not exist</h1>"


