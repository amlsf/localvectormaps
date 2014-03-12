#TODO use Javascript and AJAX????
#TODO(optional) add bunch of links to navigate better, like logout

from flask import Flask, render_template, redirect, request, session, url_for, flash
import model
import datetime

app = Flask(__name__)

app.secret_key = "secretkey"

# @app.route("/")
# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     return render_template("user_list.html", users=user_list)  

@app.route("/")
def index():
# Checks if user successfully logged in (to session), then gives update
    if session.get('user_id'):
        flash("Userid: %s, useremail: %s is logged in!"%(session['user_id'], session['useremail']))
        return redirect(url_for("view_users"))
    else:
        return render_template("index.html")


@app.route("/", methods=["POST"])
def process_login():
    useremail = request.form.get("useremail")
    password = request.form.get("password")

# Checks user authenticated to then create a session
    user = model.session.query(model.User).filter_by(email=useremail).all()

    if user == []:
        flash("Username does not exist, please register a new account")
    elif user[0].password == password:
        flash("User authenticated!")
        session['user_id'] = user[0].id
        session['useremail'] = user[0].email
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))


@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register")
def register():
    if session.get('user_id'):
        # username = session.get('username')      
        # return redirect(url_for("view_user", username = username))
        # Take the below out later
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/register", methods=["POST"])
def create_account():
    useremail = request.form.get("email")
    password = request.form.get("password")
    password_ver = request.form.get("password_verify")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    gender = request.form.get("gender")

    user = model.session.query(model.User).filter_by(email=useremail).all()

# TODO(optional)-add regex confirmation of email, validation all fields filled in & appropriately
# Verification if user already exists 
    if user != []: 
        flash("This username already exists, Please select another one!")
        return redirect(url_for("register"))
# Verification that passwords match 
    elif password != password_ver:
        flash("Your passwords do not match.")
        print  password, password_ver
        return redirect(url_for("register"))
    else:
        newperson = model.User(email=useremail, 
                            password=password, 
                            age=age, 
                            zipcode=zipcode,
                            gender=gender)
        model.session.add(newperson)
        model.session.commit()
        flash("New user was created")            
        return redirect(url_for("index"))

# TODO why is this so slow? But the view_movies is fine even though far more entries? (probably length)
@app.route("/users")
def view_users():
    if session.get('user_id'):
        users_list = model.session.query(model.User).all()
        return render_template("user_list.html", users_list=users_list)
    else:
        flash("Please login")
        return redirect(url_for("index"))

#TODO(optional) add in movie names, add hyperlinks to movies, create a handler to view all movies
@app.route("/users/<user_id>")
def user_ratings(user_id):
    if session.get('user_id'):
        user_ratings = model.session.query(model.Ratingsdata).filter_by(user_id=user_id).all()
        return render_template("user_ratings.html", user_ratings=user_ratings)
    else:
        flash("Please login")
        return redirect(url_for("index"))

@app.route("/movies")
def view_movies():
    if session.get('user_id'):
        movie_list = model.session.query(model.Movie).all()
        return render_template("movie_list.html", movie_list=movie_list)
    else:
        flash("Please login")
        return redirect(url_for("index"))



@app.route("/movie/<movie_id>", methods=["GET"])
def view_movie(movie_id):
# My code to view all the ratings for a particular movie
    movie_ratings = model.session.query(model.Ratingsdata).filter_by(movie_id=movie_id).all()
    movie = model.session.query(model.Movie).filter_by(movie_id=movie_id).one()
    movie_title = movie.title

# Extra part from Christian for predictions
# TODO - must insert a bunch of ratings for the "Eye"
# When a user views a movie they haven't rated, 
    #the Eye predicts how that user will rate that movie.
# Once a user has either rated the movie or received a prediction, 
    #the Eye will find its own rating for that movie, predicting the number if it has to.
# The Eye will take the difference of the two ratings, 
    # and criticize the user for their tastes.
    movie = session.query(model.Movie).get(movie_id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == session['user_id']:
            user_rating = r
        rating_nums.append(r.rating)
# TODO why are we creating a list to calculate average rating here? Just to display? 
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    # Prediction code: only predict if the user hasn't rated it.
    user = session.query(model.User).get(session['user_id'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
    else:
        effective_rating = user_rating.rating        
    # End prediction

    the_eye = session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
    eye_rating = session.query(model.Ratingsdata).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)


#Fix the messages syntax for error
#TODO - pass message and Jinja key-value pairs to html template 
#TODO See if you can figure out how to make the eye choose from a wider selection of messages 
    #(hint, multiply the difference by something). Then, make your eye more evil.
    messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot.",
             beratement = messages[int(difference)]

    return render_template("movie_ratings.html",
            movie_ratings=movie_ratings, 
            movie_title = movie_title, 
            movie=movie, 
            average=avg_rating, 
            user_rating=user_rating,
            prediction=prediction)

# My original stuff
# @app.route("/movies/<movie_id>")
# def movie_ratings(movie_id):
#     if session.get('user_id'):
#         movie_ratings = model.session.query(model.Ratingsdata).filter_by(movie_id=movie_id).all()
#         movie = model.session.query(model.Movie).filter_by(movie_id=movie_id).one()
#         movie_title = movie.title
#         return render_template("movie_ratings.html", movie_ratings=movie_ratings, movie_title = movie_title)
#     else:
#         flash("Please login")
#         return redirect(url_for("index"))

@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    user_id = session.get('user_id')
    rating = request.form.get("rating")
    existing = model.session.query(model.Ratingsdata).filter_by(user_id = user_id, movie_id = movie_id).all()

# TODO: validation get integer check not to crap out & check range not working
# TODO (optional) try using JS to have 5 boxes to select from

    if not rating.isdigit():
        flash("please input a valid numeric")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    if not int(rating) <= 5 or not int(rating) >= 1:
        flash ("Please enter a valid number between 1-5")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    if existing != []:
# TODO update review. How ask for user confirmation you want to change?  
        flash("You have already left a review for this movie")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    else:
        new_rating = model.Ratingsdata(movie_id = movie_id, 
            user_id = user_id, 
            rating = int(rating))
        model.session.add(new_rating)
        model.session.commit()
        flash("You have successfully added a review for this movie")
        return redirect(url_for("movie_ratings", movie_id = movie_id))

if __name__ == "__main__":
    app.run(debug = True)
