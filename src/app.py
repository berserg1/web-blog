from flask import Flask

app = Flask(__name__)  # Create a Flask app, ie an object of the Flask class


# Create app endpoints
@app.route('/')  # Could correspond to smth like www.mysite.com/api/
def hello_method():  # A simple view associated with the route
    return "Hello, world"

if __name__ == '__main__':
    app.run(port=4995)
