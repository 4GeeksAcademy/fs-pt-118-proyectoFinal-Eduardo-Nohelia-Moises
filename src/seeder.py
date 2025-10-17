import random
from api.models import db, User, Profile, Movies, Favorites, MoviesViews, Reviews, ReviewsMovieVerse
from datetime import datetime
from app import app


def seed_data():
    # === USERS ===
    users = []
    for i in range(1, 6):
        user = User(
            email=f"user{i}@example.com",
            password="pepe123",
            valoration=random.randint(0, 100)
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    # === PROFILES ===
    preferences = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror"]
    for i, user in enumerate(users, start=1):
        profile = Profile(
            username=f"User{i}",
            avatar=f"https://example.com/avatar{i}.jpg",
            preference=random.choice(preferences),
            user_id=user.id
        )
        db.session.add(profile)
    db.session.commit()

    # === MOVIES ===
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
    movies = []
    for i in range(1, 9):
        movie = Movies(
            title=f"Movie {i}",
            description=f"This is the description for Movie {i}.",
            year=random.randint(1980, 2025),
            actors=f"Actor A{i}, Actor B{i}, Actor C{i}",
            genere=random.choice(genres),
            duration=random.randint(80, 180),
            valoration=round(random.uniform(0, 10), 1),
            total_valoration=random.randint(0, 500),
            url_streaming=f"https://streaming.example.com/movie{i}"
        )
        db.session.add(movie)
        movies.append(movie)
    db.session.commit()

    # === FAVORITES ===
    for user in users:
        favorite_movies = random.sample(movies, k=random.randint(1, 3))
        for movie in favorite_movies:
            fav = Favorites(
                user_id=user.id,
                movies_id=movie.id,
                created_at=datetime.utcnow()
            )
            db.session.add(fav)
    db.session.commit()

    # === MOVIE VIEWS ===
    for user in users:
        viewed_movies = random.sample(movies, k=random.randint(2, 5))
        for movie in viewed_movies:
            mv = MoviesViews(
                user_id=user.id,
                movie_id=movie.id,
                created_at=datetime.utcnow()
            )
            db.session.add(mv)
    db.session.commit()

    # === REVIEWS ===
    review_titles = ["Good!", "Bad", "Excellent", "Meh", "Loved it", "Not my type"]
    for user in users:
        for movie in random.sample(movies, k=2):
            review = Reviews(
                title=random.choice(review_titles),
                body=f"This is a review for {movie.title} by {user.email}.",
                valoration=random.randint(1, 5),
                user_id=user.id,
                movies_id=movie.id,
                created_at=datetime.utcnow()
            )
            db.session.add(review)
    db.session.commit()

    # === REVIEWS MOVIE VERSE ===
    for user in users:
        rmv = ReviewsMovieVerse(
            title=f"Verse Review by {user.email}",
            body=f"A reflection about the cinematic universe by {user.email}.",
            valoration=random.randint(1, 5),
            user_id=user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(rmv)
    db.session.commit()

    print("✅ Database seeded successfully without Faker!")

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_data()