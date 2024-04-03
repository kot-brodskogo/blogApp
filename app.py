import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # we will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
