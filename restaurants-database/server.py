#!/usr/local/bin/python3
import http.server
import socketserver

# import the python library for SQLite 
import sqlite3

# Create Restaurant class that holds name and location
class Restaurant:
    def __init__(self, name, neighbourhood):
        self.name = name
        self.neighbourhood = neighbourhood

    # define a method to return a html list item with the name and neighbourhood
    def to_html(self):
        return f"""
        <li>
        <h3>{self.name}</h3>
        <p>{self.neighbourhood}</p>
        </li>
        """


def generate_html(restaurants):
    # add the start of the html list to restaurants_html
    restaurants_html = """<ul id="restaurants-list">"""

    # loop through restaurants...
    for restaurant in restaurants:
        # add html list item from restaurant.to_html() to restaurants_html
        restaurants_html += restaurant.to_html()

    # add the ending tag of the list to restaurants_html
    restaurants_html += """
    </ul>
    """

    # generate html string with the list from restaurants_html embedded into it
    html = f"""
    <!DOCTYPE html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
    <html lang="en-GB">
        <head>
            <title>Restaurants in Berlin</title>
            <link rel="stylesheet" type="text/css" href="./style.css">
        </head>
        <body>
            <h1>Hungry? Find some restaurants in Berlin</h1>

            <div id="restaurants-div">
            {restaurants_html}
            </div>
        </body>
    </html>
    """

    # return the html string
    return html

def get_restaurants_from_db():

    # connect to the database file, and create a connection object
    db_connection = sqlite3.connect('./restaurants.db')

    # create a database cursor object, which allows us to perform SQL on the database. 
    db_cursor = db_connection.cursor()

    # Get the restaurant name and neighbourhood name out of the database
    db_cursor.execute("SELECT restaurants.name,neighborhoods.name from restaurants LEFT JOIN neighborhoods ON restaurants.NEIGHBORHOOD_ID = neighborhoods.ID WHERE NEIGHBORHOOD_ID=1")

    # store the result in a local variable. 
    # this will be a list of tuples, where each tuple represents a row in the table
    list_restaurants = db_cursor.fetchall()

    # close the database connection
    db_connection.close()

    # return query result
    return list_restaurants


if __name__ == "__main__":

    # get restaurants_list from database
    restaurants_list = get_restaurants_from_db()

    # initialise empty list to hold the restaurants
    restaurants = []

    # loop through rows of the restaurant db query result
    for entry in restaurants_list:
        
        name = entry[0]
        neighbourhood = entry[1]

        # create new instance of Restaurant class for current restaurant
        restaurant = Restaurant(name, neighbourhood)

        # add restaurant object to restaurants list
        restaurants.append(restaurant)
    
    # generate html with restaurants
    html = generate_html(restaurants)
    
    # write html string to index.html
    with open("./index.html", "w+") as index_html:
        index_html.write(html)
    

    # Setup and run webserver
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server running on port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        