"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User,Profile,MoviesViews,Favorites,Reviews,ReviewsMovieVerse
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


#------EndPoints User----------------------------------------

@api.route('/register',methods=['POST'])
def register():
    try:
        body= request.json

        new_user = User(
            email = body['email'],
            password = body['password']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'data': 'user register, login now'}),200
    
    except Exception as error:
        return jsonify({'success': False , 'error': error}),500
    


@api.route('/login',methods=['POST'])
def login():
    try:
        body= request.json

        query= select(User).where(User.email == body['email'])
        user = db.session.execute(query).scalar_one()

        if not user:
            return jsonify({'success': False, 'user': 'no user found'}),404
        
        if user.password != body['password']:
            return jsonify({'success': False, 'user': 'email/password wrong'}),400
        
        token = create_access_token(identity=str(user.id))

        
        return jsonify({'success': True, 'token': token}),200
    
    except Exception as error:
        return jsonify({'success': False , 'error': error}),500















@api.route('/user', methods=['GET'])
def get_all_user():
    try:
        query= select(User)
        user = db.session.execute(query).scalars().all()

        if not user:
            return jsonify({'success':False, 'user':'No users'}),200
        user = [u.serialize() for u in user]

        return jsonify({'success': True, 'user':user}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    

#-----------endpoint obtener usuario por id-----------------

@api.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    try:

        user = db.session.get(User,id)

        if not user:
            return jsonify({'success':False, 'user': 'No user found'}),200
        
        return jsonify({'success':True , 'user': user.serialize()}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
        


#-------endpoint eliminar usuario----------------------------

@api.route('/user/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:

        user = db.session.get(User,id)

        if not user:
            return jsonify({'success': False, 'user':'No user'}),200
        
        db.session.delete(user)
        db.session.commit()

        return jsonify({'success':True, 'user': 'user delete'}),200
    
    except Exception as error:
        return jsonify({'success':False, 'error':error}),500
    

#----------------endpoints profile--------------------------------------

@api.route('/profile', methods=['GET'])
def get_all_profile():
    try:
        query=select(Profile)
        profile = db.session.execute(query).scalars().all()

        if not profile:
            return jsonify({'success': False, 'profile': 'no profiles'}),200
        
        profile = [p.serialize() for p in profile]
        return jsonify({'success': True, 'profile':profile}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    
#------------------endpoint obtener perfil por username-----------------------

@api.route('/profile/<username>', methods=['GET'])
def get_one_profile_by_name(username):
    try:
        query= select(Profile).where(Profile.username == username)
        profile = db.session.execute(query).scalars().all()
        profile = [p.serialize() for p in profile]

        if not profile:
            return jsonify({'success': False, 'profile':'No profile found'}),200
        
        return jsonify({'success': True, 'profile':profile}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error': error}),500
    

#-----------------endpoint obtener perfil por id------------------------------

@api.route('/profile/<int:id>', methods=['GET'])
def get_one_profile(id):
    try:

        profile = db.session.get(Profile,id)

        if not profile:
            return jsonify({'success':False, 'profile': 'No profile found'}),200
        
        return jsonify({'success':True , 'profile': profile.serialize()}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    


#------------endpoint modificar perfil----------------------------------------

@api.route('/profile/<int:id>', methods=['PUT'])
def update_profile(id):
    try:
        body = request.json

        profile = db.session.get(Profile,id)
        if not profile:
            return jsonify({'success':False, 'profile':'profile not Found'})
        
        profile.username = body.get('username') or profile.username
        profile.avatar = body.get('avatar') or profile.avatar
        profile.preference = body.get('preference') or profile.preference
        

     
        db.session.commit()
    
        return jsonify({'success': True, 'profile':profile.serialize()}),200
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error})
    
    


#----------------endpoints favorites------------------------------------------------------------



@api.route('/favorites', methods=['GET'])
def get_all_favorites():
    try:
        query=select(Favorites)
        favorites = db.session.execute(query).scalars().all()

        if not favorites:
            return jsonify({'success': False, 'favorites': 'no favorites'}),200
        
        favorites = [f.serialize() for f in favorites]
        return jsonify({'success': True, 'favorites':favorites}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    

#----------------endpoint obtener favoritos por id------------------------------------------

@api.route('/favorites/<int:id>', methods=['GET'])
def get_one_favorites(id):
    try:
       
        favorites= db.session.get(Favorites,id)

        if not favorites:
            return jsonify({'success':False, 'data':'No favorites found'}),200

        return jsonify({'success': True, 'data':favorites.serialize()}),200
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    

#-----------------endpoint crear un favorito-----------------------------------------------

@api.route('/favorites', methods=['POST'])
def create_favorites():
    try:
        body = request.json

    
        new_favorites= Favorites(
            user_id=body['user_id'],
            tmdb_id=body['tmdb_id'],
        )
        db.session.add(new_favorites)
        db.session.commit()
    
        return jsonify({'success': True, 'data':new_favorites.serialize()}),201
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error}),500
    


#---------------endpoint eliminar favorito----------------------------------------

@api.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorites(id):
    try:
       
        favorites= db.session.get(Favorites,id)

        if not favorites:
            return jsonify({'success':False, 'favorites':'No favorites found'}),200
        
        db.session.delete(favorites)
        db.session.commit()

        return jsonify({'success': True, 'data':'favorites delete'}),200
    except Exception as error:
        return jsonify({'success': False, 'error':error})
    


#----------------------endpoints reviews---------------------------------------------------------


#------endpoint para obtener todos las reseñas--------------------------------------
@api.route('/reviews', methods=['GET'])
def get_all_reviews():
    try:
        query=select(Reviews)
        reviews = db.session.execute(query).scalars().all()

        if not reviews:
            return jsonify({'success': False, 'reviews': 'no reviews'}),200
        
        reviews = [r.serialize() for r in reviews]
        return jsonify({'success': True, 'reviews':reviews}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    


#------------endpoints para obtener reseñas por peliculas----------------------

@api.route('/reviews/<int:tmdb_id>', methods=['GET'])
def get_movies_reviews(tmdb_id):
    try:
        query= select(Reviews).where(Reviews.tmdb_id == tmdb_id)
        reviews = db.session.execute(query).scalars().all()
        reviews = [r.serialize() for r in reviews]

        if not reviews:
            return jsonify({'success': False, 'reviews':'No reviews found'}),200
        
        return jsonify({'success': True, 'reviews':reviews}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error': error}),500
    

#---------------endpoints para crear reseñas de peliculas---------------------------------

@api.route('/reviews', methods=['POST'])
def create_reviews():
    try:
        body = request.json

    
        reviews= Reviews(
            title=body['title'],
            body=body['body'],
            valoration=body['valoration',0],
            user_id=body['user_id'],
            tmdb_id=body['tmdb_id']
            
        )
        db.session.add(reviews)
        db.session.commit()
    
        return jsonify({'success': True, 'reviews':reviews.serialize()}),201
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error}),500
    


#---------------endpoints para modificar reseñas de peliculas-------------------------------------

@api.route('/reviews/<int:id>', methods=['PUT'])
def update_reviews(id):
    try:
        body = request.json

        reviews = db.session.get(Reviews,id)
        if not reviews:
            return jsonify({'success':False, 'reviews':'reviews not Found'})
        
        reviews.title = body.get('title') or reviews.title
        reviews.body = body.get('body') or reviews.body
        reviews.valoration = body.get('valoration') or reviews.valoration
        

     
        db.session.commit()
    
        return jsonify({'success': True, 'reviews':reviews.serialize()}),200
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error})
    
#---------------------endpoints para eliminar reseñas------------------------------------------------

@api.route('/reviews/<int:id>', methods=['DELETE'])
def delete_reviews(id):
    try:
       
        reviews= db.session.get(Reviews,id)

        if not reviews:
            return jsonify({'success':False, 'reviews':'No reviews found'}),200
        
        db.session.delete(reviews)
        db.session.commit()

        return jsonify({'success': True, 'data':'reviews delete'}),200
    except Exception as error:
        return jsonify({'success': False, 'error':error})
    



#---------------------------------------------endpoints ReviewsMovieVerse------------------------------------------------------------


#----------------endpoints para obtener todas las reseñas de movieverse---------------------------------------

@api.route('/movieverse', methods=['GET'])
def get_all_reviews_movie_verse():
    try:
        query=select(ReviewsMovieVerse)
        reviews_movie_verse = db.session.execute(query).scalars().all()

        if not reviews_movie_verse:
            return jsonify({'success': False, 'reviews': 'no reviews'}),200
        
        reviews_movie_verse = [r.serialize() for r in reviews_movie_verse]
        return jsonify({'success': True, 'reviews_movie_verse':reviews_movie_verse}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    

#-------------------endpoints para crear reseñas movieverse---------------------------------------------


@api.route('/movieverse', methods=['POST'])
def create_reviews_movieverse():
    try:
        body = request.json

    
        reviews_movie_verse= ReviewsMovieVerse(
            title=body['title'],
            body=body['body'],
            valoration=body['valoration',0],
            user_id=body['user_id']
        )
        db.session.add(reviews_movie_verse)
        db.session.commit()
    
        return jsonify({'success': True, 'reviews':reviews_movie_verse.serialize()}),201
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error}),500
    


#--------------endpoint para modificar reseñas movieverse---------------------------------------------



@api.route('/movieverse/<int:id>', methods=['PUT'])
def update_reviews_movieverse(id):
    try:
        body = request.json

        reviews_movie_verse = db.session.get(ReviewsMovieVerse,id)
        if not reviews_movie_verse:
            return jsonify({'success':False, 'reviews':'reviews not Found'})
        
        reviews_movie_verse.title = body.get('title') or reviews_movie_verse.title
        reviews_movie_verse.body = body.get('body') or reviews_movie_verse.body
        reviews_movie_verse.valoration = body.get('valoration') or reviews_movie_verse.valoration
        

     
        db.session.commit()
    
        return jsonify({'success': True, 'reviews_movie_verse':reviews_movie_verse.serialize()}),200
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error})
    


#----------------endpoint para eliminar reseñas movieverse---------------------------------------------


@api.route('/movieverse/<int:id>', methods=['DELETE'])
def delete_reviews_movieverse(id):
    try:
       
        reviews_movie_verse= db.session.get(ReviewsMovieVerse,id)

        if not reviews_movie_verse:
            return jsonify({'success':False, 'reviews':'No reviews found'}),200
        
        db.session.delete(reviews_movie_verse)
        db.session.commit()

        return jsonify({'success': True, 'reviews':'reviews delete'}),200
    except Exception as error:
        return jsonify({'success': False, 'error':error})




#---------------------------endpoint peliculasvista casi se me olvidan xD -----------------------------

@api.route('/moviesviews', methods=['GET'])
def get_all_movieviews():
    try:
        query=select(MoviesViews)
        movies_views = db.session.execute(query).scalars().all()

        if not movies_views:
            return jsonify({'success': False, 'movies views': 'no movies views'}),200
        
        movies_views = [m.serialize() for m in movies_views]
        return jsonify({'success': True, 'movie views':movies_views}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    

#----------------endpoint para obtener peliculas vistas por id--------------------------------------

@api.route('/moviesviews/<int:id>', methods=['GET'])
def get_one_moviesviews(id):
    try:

        movies_views = db.session.get(MoviesViews,id)

        if not movies_views:
            return jsonify({'success':False, 'movies views': 'No movies views found'}),200
        
        return jsonify({'success':True , 'movies views': movies_views.serialize()}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error':error}),500
    


#--------------------------endpoint para obtener peliculas vistas por titulo------------------------------


@api.route('/moviesviews/<title>', methods=['GET'])
def get_one_moviesviews_by_title(title):
    try:
        query= select(MoviesViews).where(MoviesViews.title == title)
        movies_views = db.session.execute(query).scalars().all()
        movies_views = [m.serialize() for m in movies_views]

        if not movies_views:
            return jsonify({'success': False, 'movies views':'No movies views found'}),200
        
        return jsonify({'success': True, 'movies views':movies_views}),200
    
    except Exception as error:
        return jsonify({'success': False, 'error': error}),500




#----------------endpoint para crear peliculas vistas------------------------------------------------------


@api.route('/moviesviews', methods=['POST'])
def create_moviesviews():
    try:
        body = request.json

    
        movies_views= MoviesViews(
            user_id=body['user_id'],
            tmdb_id=body['tmdb_id']
        )
        db.session.add(movies_views)
        db.session.commit()
    
        return jsonify({'success': True, 'movies views':movies_views.serialize()}),201
    except Exception as error:
        db.session.rollback()
        return jsonify({'success': False, 'error':error}),500




#------------------endpoint para eliminar peliculas vistas---------------------------------------


@api.route('/moviesviews/<int:id>', methods=['DELETE'])
def delete_moviesviews(id):
    try:
       
        movies_views= db.session.get(MoviesViews,id)

        if not movies_views:
            return jsonify({'success':False, 'movies views':'No movies views found'}),200
        
        db.session.delete(movies_views)
        db.session.commit()

        return jsonify({'success': True, 'movie views':'movies views delete'}),200
    except Exception as error:
        return jsonify({'success': False, 'error':error})