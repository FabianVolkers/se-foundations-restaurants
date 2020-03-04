#!/usr/local/bin/python3
import http.server
import socketserver

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
    


def create_restaurant(csv_entry):
    # Replace unwanted newline with nothing
    csv_entry = csv_entry.replace("\n", "")
    # Separate entry at comma
    csv_entry = csv_entry.split(",")
        
    name = csv_entry[0]
    neighbourhood = csv_entry[1]

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


if __name__ == "__main__":

    # open restaurants.txt and read its contents
    with open("./restaurants.txt", "r") as restaurants_file:
        restaurants_list = restaurants_file.readlines()

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
        