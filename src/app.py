from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.user import User

app = Flask(__name__)  # Create a Flask app, ie an object of the Flask class
app.secret_key = "test"  # This insecure key is just for testing purposes


# Create app endpoints
@app.route('/')
def home_template():
    return  render_template('home.html')


@app.route('/login')  # Route or endpoint, like mysite.com/api/login
def login_template():  # A view associated with the route
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')

@app.before_first_request  # This decorator will allow DB init before first request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])  # This route will accept only post requests
def login_user():
    email = request.form['email']  # request data from request.form dictionary
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None  # if the user login is not valid, remove email from session

    return render_template("profile.html", email=session['email'])  # Render template with some data from session

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])

if __name__ == '__main__':
    app.run(port=4995)
