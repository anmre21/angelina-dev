import flask
import flask_flatpages

# Config
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'src'
FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code', 'codehilite']

app = flask.Flask(__name__)
app.config.from_object(__name__)
flatpages = flask_flatpages.FlatPages(app)

@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("index.html")

@app.route("/blog")
def blog():
    posts = [p for p in flatpages]
    posts = sorted(posts, reverse=True, key=lambda p: p.meta["published"])
    return flask.render_template("blog.html", posts=posts)

@app.route("/blog/<name>")
def blog_post(name):
    post = flatpages.get_or_404(name)
    return flask.render_template("blog_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)