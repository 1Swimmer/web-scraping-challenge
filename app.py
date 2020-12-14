from flask import Flask, render_template, redirect
from pymongo import MongoClient
import scrape_mars



# Use flask_pymongo to set up mongo connection
mongo = MongoClient("mongodb://localhost:27017/marsmission_app")

# Create an instance of Flask
app = Flask(__name__)

@app.route("/")
def index():
    marsdata = mongo.db.marsdata.find_one()
    return render_template("index.html", marsdata=marsdata)


@app.route("/scrape")
def scraper():
    marsdata = mongo.db.marsdata
    mars_data=scrape_mars.scrape()
    marsdata.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

    
if __name__ == "__main__":
    app.run(debug=True)