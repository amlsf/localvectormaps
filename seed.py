# For loading data into the database once it's been set up and tables created from model.py
import model
import csv
import datetime
import re


def load_users(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter = "|")
        for row in reader:
# This creates a tuple 
            id, age, gender, profession, zipcode = row
            id = int(id)
            age = int(age)
            u = model.User(id = id, 
                age = age,
                zipcode =zipcode,
                gender = gender,
                email = None,
                password = None)
            session.add(u)

    session.commit()
    f.close()

def load_movies(session):

    moviefile = open("seed_data/u.item") 

    for row in moviefile:  
        row = row.split("|")
        print row
        movie_id, title, released, other, url = row[:5]
        movie_id = int(movie_id)
        if released == '':
            movieitem = model.Movie(movie_id = movie_id, 
                    title = title,
                    released = datetime.datetime.strptime("01-Jan-1970", "%d-%b-%Y"),
                    url = "unknown")
        else:         
            releasedate = datetime.datetime.strptime(released, "%d-%b-%Y")
            title = re.sub("\s\(\d{4}\)", "", title)

            # title = title.split(" (")
            # title = title[0]
# TODO this latin-1 seems to be limiting the movie title characters
            title = title.decode("latin-1")
            movieitem = model.Movie(movie_id = movie_id,
                    title = title, 
                    released = releasedate, 
                    url = url)

        session.add(movieitem)

    session.commit()
    moviefile.close()

def load_ratings(session):
    ratingfile = open("seed_data/u.data") 

    for ratingline in ratingfile:  
        ratingline = ratingline.split("\t")
        user_id, item_id, rating, timestamp = ratingline
        rating = int(rating)
        user_id = int(user_id)
        item_id = int(item_id)
        ratingitem = model.Ratingsdata(movie_id = item_id, 
            user_id = user_id, 
            rating = rating)
        session.add(ratingitem)

    session.commit()
    ratingfile.close()


def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
