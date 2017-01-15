from flask import Flask, render_template

app = Flask(__name__)  # Create a Flask app, ie an object of the Flask class


# Create app endpoints
@app.route('/')  # Could correspond to smth like www.mysite.com/api/
def hello_method():  # A simple view associated with the route
    return render_template('login.html')

if __name__ == '__main__':
    app.run(port=4995)
