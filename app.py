from this import d
from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


@app.route("/", methods=["POST", "GET"])
def hello_world():
  if request.method == "POST":
      return {
          "long_url": request.form["url"]
        }
  else:
      return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
