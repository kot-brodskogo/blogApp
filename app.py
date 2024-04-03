import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class BlogManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.blog_posts = []  # Initialize blog_posts as an empty list
        self.load_posts()

    def load_posts(self):
        with open(self.data_file, 'r') as f:
            self.blog_posts = json.load(f)

    def save_posts(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.blog_posts, f, indent=4)

    def add_post(self, new_post):
        self.blog_posts.append(new_post)
        self.save_posts()

    def delete_post(self, post_id):
        self.blog_posts = [post for post in self.blog_posts if str(post['id']) != post_id]
        self.save_posts()


blog_manager = BlogManager('blog_data.json')


@app.route('/')
def index():
    return render_template('index.html', posts=blog_manager.blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Extract data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Generate a unique ID for the new blog post
        new_id = generate_unique_id()

        # Create a new blog post object
        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content
        }

        # Add the new blog post using the BlogManager instance
        blog_manager.add_post(new_post)

        # Redirect to the index page after adding the new blog post
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    blog_manager.delete_post(post_id)
    return redirect(url_for('index'))


def generate_unique_id():
    # Generate a UUID and return its hexadecimal representation
    return uuid.uuid4().hex


if __name__ == '__main__':
    app.run(debug=True)
