#!/usr/local/bin/python3
import http.server
import socketserver

# import the python library for SQLite 
import sqlite3

class Restaurant:
    def __init__(self, name, neighbourhood):
        self.name = name
        self.neighbourhood = neighbourhood

    def to_html(self):
        return f"""
        <li>
        <h3>{self.name}</h3>
        <p>{self.neighbourhood}</p>
        </li>
        """
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def __str__(self):
        return f"Restaurant:\nName: {self.name}\nLocation: {self.neighbourhood}"
    


def create_restaurant(db_entry):

        
    name = db_entry[0]
    neighbourhood = db_entry[1]

    return Restaurant(name, neighbourhood)


def generate_html(restaurants):

    restaurants_html = """<ul id="restaurants-list">"""

    for restaurant in restaurants:
        restaurants_html += restaurant.to_html()

    restaurants_html += """
    </ul>
    """

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
    return html

def get_restaurants_from_db():

    # connect to the database file, and create a connection object
    db_connection = sqlite3.connect('./restaurants.db')

    # create a database cursor object, which allows us to perform SQL on the database. 
    db_cursor = db_connection.cursor()

    # run a first query 
    db_cursor.execute("SELECT restaurants.name,neighborhoods.name from restaurants LEFT JOIN neighborhoods ON restaurants.NEIGHBORHOOD_ID = neighborhoods.ID WHERE NEIGHBORHOOD_ID=1")

    # store the result in a local variable. 
    # this will be a list of tuples, where each tuple represents a row in the table
    list_restaurants = db_cursor.fetchall()


    db_connection.close()

    return list_restaurants


if __name__ == "__main__":

    restaurants_list = get_restaurants_from_db()

    # initialise empty list to hold the restaurants
    restaurants = []

    # loop through rows of the restaurants file's content
    for entry in restaurants_list:
        
        restaurant = create_restaurant(entry)
        restaurants.append(restaurant)
    
    html = generate_html(restaurants)
    
    with open("./index.html", "w+") as index_html:
        index_html.write(html)
    
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server running on port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        