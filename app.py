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
        post_to_delete = self.fetch_post_by_id(post_id)
        if post_to_delete:
            self.blog_posts.remove(post_to_delete)
            self.save_posts()

    def fetch_post_by_id(self, post_id):
        for post in self.blog_posts:
            if str(post['id']) == post_id:
                return post
        return None


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


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = blog_manager.fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details based on the form submission
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Update the post details
        post['title'] = title
        post['author'] = author
        post['content'] = content

        # Save the updated blog posts to the JSON file
        blog_manager.save_posts()

        # Redirect back to the index page
        return redirect(url_for('index'))

    # If it's a GET request, display the update form
    return render_template('update.html', post=post)


def generate_unique_id():
    # Generate a UUID and return its hexadecimal representation
    return uuid.uuid4().hex


if __name__ == '__main__':
    app.run(debug=True)
