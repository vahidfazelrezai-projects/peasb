from flask import Flask
app = Flask(__name__)

@app.route('/moose/')
def hello():
    """Return a friendly HTTP greeting."""
    return '<h1>Hello Moose!</h1>'
