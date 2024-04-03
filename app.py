import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


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

        # Read existing blog posts from the JSON file
        with open('blog_data.json', 'r') as f:
            blog_posts = json.load(f)

        # Append the new blog post to the list of existing blog posts
        blog_posts.append(new_post)

        # Write the updated list of blog posts back to the JSON file
        with open('blog_data.json', 'w') as f:
            json.dump(blog_posts, f, indent=4)

        # Redirect to the index page after adding the new blog post
        return redirect(url_for('index'))
    return render_template('add.html')


def generate_unique_id():
    # Generate a UUID and return its hexadecimal representation
    return uuid.uuid4().hex


if __name__ == '__main__':
    app.run()
