# Import Dependencies 
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import scrape_mars



# Create an instance of Flask app
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info = mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrape function
    data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, data, upsert=True)
    return 'All done!'

if __name__ == "__main__": 
    app.run(debug= True)