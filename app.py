import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
