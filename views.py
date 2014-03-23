from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model

app = Flask(__name__)
app.config.from_object(config)

model.session = model.connect()

# Stuff to make login easier
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

app.secret_key = "secretkey"


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# # End login stuff

# # Adding markdown capability to the app
# Markdown(app)

@app.route("/")
def index():
    # active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
    return render_template("heatmap.html", active_listings = [])

@app.route("/activelistings")
def activelistings():
    active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
    # some_json = '{"liz" : "is tired"}'
    # # json = JSON.dumps([x.to_json() for x in activelistings])
    # some_json=some_json
    return render_template("heatmap.html", active_listings = active_listings)

@app.route("/leaflet")
def leaflet():
    active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
    activelatlong = [[l.latitude, l.longitude] for l in active_listings]
    return render_template("leaflet.html", activelatlong = activelatlong)

# @app.route("/heatmap")
# def leaflet():
#     active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
#     activelatlong = [[l.latitude, l.longitude] for l in active_listings]
#     return render_template("leaflet.html", activelatlong = activelatlong)




# @app.route("/medianprices")
# def medianprices(grouping, activeornot):
#     active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
#     return render_template("heatmap.html", active_listings = active_listings)

# select all median prices by grouping type, active vs. not active




    # return "[{\"address\": \"drive\"}]" #This is JSON array, turns to JS syntax, use with AJAX stuff in main.js


# @app.route("/medianpricechange")


# @app.route("/post/<int:id>")
# def view_post(id):
#     post = Post.query.get(id)
#     return render_template("post.html", post=post)

# @app.route("/post/new")
# @login_required
# def new_post():
#     return render_template("new_post.html")

# @app.route("/post/new", methods=["POST"])
# @login_required
# def create_post():
#     form = forms.NewPostForm(request.form)
#     if not form.validate():
#         flash("Error, all fields are required")
#         return render_template("new_post.html")

#     post = Post(title=form.title.data, body=form.body.data)
#     current_user.posts.append(post) 
    
#     model.session.commit()
#     model.session.refresh(post)

#     return redirect(url_for("view_post", id=post.id))

# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def authenticate():
#     form = forms.LoginForm(request.form)
#     if not form.validate():
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     email = form.email.data
#     password = form.password.data

#     user = User.query.filter_by(email=email).first()

#     if not user or not user.authenticate(password):
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     login_user(user)
#     return redirect(request.args.get("next", url_for("index")))


if __name__ == "__main__":
    app.run(debug=True)
