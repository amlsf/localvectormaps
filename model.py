from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

# NOTES
# Table  <->  Class
# Column <->  Attribute
# Row    <->  Instance
# The below create a table (or class)

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

# This is what we use to later declare a class to be managed by SQLAlchemy
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    gender = Column(String(5), nullable = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)

    # data = relationship("Data", order_by = movies_id")

    def similarity(self, other_user):
        u_ratings = {}
        paired_ratings = []
# same thing as: user1_ratings = session.query(Ratingsdata).filter_by(user_id = user1_id).all()
        for r in self.ratings: # this is backref the connection between user and ratings table
            u_ratings[r.movie_id] = r

# same thing as: user2_ratings = session.query(Ratingsdata).filter_by (user_id = user2_id).all()
        for r in other_user.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

# Rank users based on similarity coefficient
    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator
        

        # other_users = [ r.user for r in other_ratings ]
        # similarities = [ (self.similarity(other_user), r) for r in other_ratings ]
        # similarities.sort(reverse = True)
        # top_user = similarities[0]
        # return top_user[1].rating * top_user[0]


        # matched_rating = None
        # for rating in other_ratings:
        #     if rating.user_id == top_user[1].id:
        #         matched_rating = rating
        #         break
        # return matched_rating.rating * top_user[0]

# NOTE: to use similarity method, other_users is list of users that have rated the movie, then: 
    # m = session.query(Movie).filter_by(title="Toy Story").one()
    # u = session.query(User).get(1)
    # ratings = u.ratings # Don't need this????

    # other_ratings = session.query(Rating).filter_by(movie_id=m.id).all()
    # other_users = []
    # for r in other_ratings:
    #     other_users.append(r.user)

class Ratingsdata(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

# Note: Many to one - the backref now creates a user (child) attribute referencing the ratings table (parent)
    # r = session.query(Rating).get(1) (get 1st rating object)
    # u = r.user (get user object associdated with rating) --> u.age, etc,
    # Can go either way like user.ratings or ratings.user  or  r.movie.title or r.user.email 
        # then can "back reference" to ratings in ratings table associated with user object like u.ratings[0].movie_id
        # convenient shortcut to put all in one parent class if it changes
    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=True)
    released = Column(DateTime, nullable=True)
    url = Column(String(64), nullable=True)

# TODO - where to do inheritance? Make sure this works - the Movie correlative 
    # prediction method gives very diff answer than User correlative prediction method? 

# pair ratings for two movies by user
# get similarty of pair 
    def similarity(self, other_movie):
        # print other_movie.title
        m_ratings = {}
        paired_ratings = []
        for r in self.ratings: # this is backref the connection between user and ratings table
            m_ratings[r.user_id] = r
            # print (r.user_id, r.rating)
            # print m_ratings

        for r in other_movie.ratings:
            # print r
            u_r = m_ratings.get(r.user_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0


    def predict_rating(self, user):
# TEST THIS
        ratings = user.ratings
# create list of movies user has already rated to list user_movies
        user_movies = [r.movie for r in ratings]

#for item in user_movies:
    # loop through to run similarity of user_movies and movie input
        similarities = [(self.similarity(movie), movie) for movie in user_movies]
        similarities.sort(reverse=True)

# find max movie similiarty
# find user's movie rating for that max movie and multiply by similarity to get prediction

        top_movie = similarities[0]
        # return user.id        
        # return top_movie[1].movie_id        
        ur_top_movie = session.query(Ratingsdata).filter_by(user_id=user.id, movie_id=top_movie[1].movie_id).one()
        # return ur_top_movie.movie.title
        # return ur_top_movie.rating
        # return top_movie[0]
        return top_movie[0] * ur_top_movie.rating

def main(session):

    u = session.query(User).get(1)
    m = session.query(Movie).get(300)
    print u.predict_rating(m)

    # u = session.query(User).get(1)
    # m = session.query(Movie).get(300)
    # print m.predict_rating(u)


if __name__ == "__main__":
    # session = connect()
    main(session)



# NOTE: This translates the above python metadata code to SQl to create the tables
    # Once create, table = class, the attributes =  columns, row = instance
    # echo = False makes it stop printing the SQl translation
# python -i model.py
# engine = create_engine("sqlite:///ratings.db", echo=False)
# Base.metadata.create_all(engine)


# NOTE: This is similar to DB.connect() to connect to the database, equivalent to session
# session = connect()

# NOTE: to modify, must pull object out, then modify, then commit
# c = session.query(User).get(1)
# c.password = "somethingmoresecure"
# session.commit()

# NOTE: must create object, then be explicit about adding, then commit
# session.add(charles)
# session = connect()


# datetime.datetime.strptime("01-Jan-1994", "%d-%b-%Y")