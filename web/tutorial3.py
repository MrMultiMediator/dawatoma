from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    cities = ['Albuquerque','Santa Fe', 'Las Cruces']
    #return "Hello! This is the main page <h1>HELLO</h1>"
    return render_template("index.html", content=name, cities=cities)



if __name__ == '__main__':
    app.run()