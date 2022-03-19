# import dependencies 
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

# set up App routes

#define the route for the HTML page
#define the route
@app.route("/")
# define what will be displayed at the route above
def index():
    #use pyMongo to find the "mars" collection in the database.
    mars=mongo.db.mars.find_one()
    #Flask will rutrn an html template, wsing the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

#add the next route and function
@app.route("/scrape")
def scrape():
    #point to our mongo database
    mars=mongo.db.mars
    #create new variable to hold newly scraped data
    mars_data=scraping.scrape_all()
    # insert data if identical record does not already exist
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect("/", code=302)

    #tell flask to run
    if __name__ == "__main__":
        app.run()