from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def displayHBNB():
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def displayC(text):
    return "C {}".format(text.translate(str.maketrans('_', ' ')))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)