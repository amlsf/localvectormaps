from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model

app = Flask(__name__)
app.config.from_object(config)

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
    return render_template("heatmap.html")

@app.route("/activelistings")
def activelistings():
    active_listings = model.session.query(model.Listings).filter_by(listing_status="Active").all()
    return render_template("heatmap.html", active_listings = active_listings)
    # return "[{\"address\": \"drive\"}]" #This is JSON array, turns to JS syntax, use with AJAX stuff in main.js

# @app.route("/medianactive")


# @app.route("/mediansold")
#     def medianprice(pricetype, ) 


# @app.route("/medianpricechange")


#Calcs needed (functions):
#1) View active listings as markers and display info as listings (ajax to certain region in map frame)
#2) Get median ACTIVE LISTING prices by various groupings (display summary table of stats)
#3) Get median SOLD SALES prices (not listing) by various groupings & time periods (display summary table of stats)
#4) can get change % later from #3?

#A) Grouping various metrics by [property type, bed/bath count], [living_sq ft range, PRICE RANGE], [city, count, neighborhood, zip]
# TODO can I put these all as arguments in the same function? how do this efficiently? 


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
