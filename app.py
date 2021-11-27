import flask

app = flask.Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run()