from flask import Flask
from models import db, Post
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

@app.route('/')
def index():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts_data = response.json()

    for post_data in posts_data:
        new_post = Post(id=post_data['id'], title=post_data['title'], body=post_data['body'])
        db.session.add(new_post)
    
    db.session.commit()
    
    return 'Data has been fetched and saved to the database!'

if __name__ == '__main__':
    app.run(debug=True)
