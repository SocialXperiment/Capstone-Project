from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"topics": [], "posts": []}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    posts = sorted(data['posts'], key=lambda x: x['timestamp'], reverse=True)
    return render_template('index.html', posts=posts[:3])

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    data = load_data()
    if request.method == 'POST':
        new_topic = request.form.get('topic')
        if new_topic:
            data['topics'].append(new_topic)
            save_data(data)
        return redirect(url_for('topics'))
    return render_template('topics.html', topics=data['topics'])

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    data = load_data()
    if request.method == 'POST':
        title = request.form.get('title')
        topic = request.form.get('topic')
        content = request.form.get('content')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_post = {
            "id": len(data['posts']) + 1,
            "title": title,
            "topic": topic,
            "content": content,
            "timestamp": timestamp
        }
        data['posts'].append(new_post)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add_post.html', topics=data['topics'])

@app.route('/post/<int:post_id>')
def post(post_id):
    data = load_data()
    post = next((p for p in data['posts'] if p['id'] == post_id), None)
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
