from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
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


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:  # If a user_id is not None, we access first route
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(email=session['email'])  # This way we are accessing our own blogs

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    # If method is GET, we need to send a form for a user to fill
    # in order to create a new blog
    if request.method == 'GET':
        # TODO after a user creates a blog, we need to change a route from blogs/new to blogs
        return render_template('new_blog.html')
    # If method is POST, we need to accept the data sent to this endpoint
    # And create new blog based on that data
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        # make_response function allows us to redirect a user to another route
        # this function takes another function (view) as a parameter
        return make_response(user_blogs(user._id))



@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts.html", posts=posts, blog_title=blog.title, blog_id=blog._id)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)

    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        # make_response function allows us to redirect a user to another route
        # this function takes another function (view) as a parameter
        return make_response(blog_posts(blog_id))

if __name__ == '__main__':
    app.run(port=4995, debug=True)
