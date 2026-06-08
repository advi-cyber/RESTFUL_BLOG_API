from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Blog Table
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Create Database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Blog API Running"

# CREATE POST
@app.route('/posts', methods=['POST'])
def create_post():

    data = request.get_json()

    new_post = Blog(
        title=data['title'],
        content=data['content']
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "message": "Post created successfully"
    })

# GET ALL POSTS
@app.route('/posts', methods=['GET'])
def get_posts():

    posts = Blog.query.all()

    result = []

    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })

    return jsonify(result)

# GET SINGLE POST
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):

    post = Blog.query.get(id)

    if not post:
        return jsonify({
            "message": "Post not found"
        }), 404

    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content
    })

# UPDATE POST
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):

    post = Blog.query.get(id)

    if not post:
        return jsonify({
            "message": "Post not found"
        }), 404

    data = request.get_json()

    post.title = data['title']
    post.content = data['content']

    db.session.commit()

    return jsonify({
        "message": "Post updated successfully"
    })

# DELETE POST
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):

    post = Blog.query.get(id)

    if not post:
        return jsonify({
            "message": "Post not found"
        }), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "message": "Post deleted successfully"
    })

if __name__ == '__main__':
    app.run(debug=True)