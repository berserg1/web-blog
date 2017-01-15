import uuid  # Universally Unique Identifier Module
from src.common.database import Database
import datetime


class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id  # uuid4 gets random id

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        """returns json representation of a post"""
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        """returns a particular post from a DB"""
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)  # Using kwargs, passing corresponding values from DB to constructor

    @staticmethod
    def from_blog(id):
        """returns a list of posts from a particular blog"""
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
