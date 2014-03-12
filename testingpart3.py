
# Calculate the pearson score
# num_critics = len(common_critics)
# num = product_sum - ((film1_sum * film2_sum)/num_critics)
# den = sqrt((film1_sum_square - pow(film1_sum, 2) / num_critics) * \
#     (film2_sum_square - pow(film2_sum, 2)/num_critics))
# pearson = num/den


# get Toy Story movie
m = session.query(Movie).filter_by(title = "Toy Story").one()
# know user 1 has NOT rated Toy Story
u = session.query(User).get(1)
# Get list of ratings from user 1
ratings = u.ratings
# Create list of users who HAVE rated Toy Story
other_ratings = session.query(Rating).filter_by(movie_id=m.movie_id).all()
other_users = []
for r in other_ratings:
    other_users.append(r.user)
# Derive correlation and predict User1 Toy Story rating by iterating through user1 ratings
    # and compare/pair to each of user2 ratings for same movies
o = other_users[0]
paired_ratings = []
for r1 in u.ratings:
    for r2 in o.ratings:
        if r1.movie_id == r2.movie_id:
            paired_ratings.append((r1.rating,r2.rating))


# Better Method with dictionary
# NOTE- wait, but isn't this different from method above in terms of going through all the movies? 
    # or still need to pull a list of user2 that have rated the movie you're looking at? 
# ANSWER (pseudocode): 
    # starting off with movie want to predict for user 1
    # select list of user2's who have rated that movie 
    # pair up movies and get correlation with each user
u_ratings = {}
for r in u.ratings:
     u_ratings[ r.movie_id ] = r
paired_ratings = []
for o_rating in o.ratings:
     u_rating = u_ratings.get(o_rating.movie_id)
     if u_rating:
         pair = (u_rating.rating, o_rating.rating)
         paired_ratings.append(pair)




# My ATTEMPT
# user1 - user trying to predict rating for a particular movie
# user2 (list) - user from a list of users that HAVE already rated that particular movie

# # gets all the movie and ratings of user 1
# for u1 in user1_ratings:
#     print u1.movie_id, u1.rating

# # gets all the movie and ratings of user 2
# for u2 in user2_ratings:
#     print u2.movie_id. u2.rating

user1_ratings = session.query(Ratingsdata).filter_by(user_id = user1_id).all()
user2_ratings = session.query(Ratingsdata).filter_by (user_id = user2_id).all()

u1_ratings_dict = {}
for u1 in user1_ratings:
    u1_ratings_dict[u1.movie_id] = u1.rating

paired_ratings = []
for u2 in user2_ratings: 
    u1rating = u1_ratings_dict.get(u2.movie_id):
    if u1rating:
        paired_ratings.append((u1rating, u2.rating))


if paired_ratings: 
    return correlation.pearson(paired_ratings)
else: 
    return(0.0)