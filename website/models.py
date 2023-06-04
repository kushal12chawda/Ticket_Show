from . import db
from flask_login import UserMixin 

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150),unique=True)
    user_email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150),unique=True)
    user_city = db.Column(db.String(150))
    def get_id(self):
        return (self.user_id)

class Admin(db.Model,UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(150),unique=True)
    admin_email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150),unique=True)
    admin_city = db.Column(db.String(150))
    def get_id(self):
        return (self.admin_id)


class Movie(db.Model, UserMixin):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(150))
    movie_release_date = db.Column(db.String(150))
    movie_ticket_cost = db.Column(db.Integer)
    movie_show_time = db.Column(db.String(150))
    movie_tag = db.Column(db.String(150))
    movie_venue = db.Column(db.String(150))
    movie_capacity = db.Column(db.Integer)
    movie_rating = db.Column(db.Integer)
    movie_length = db.Column(db.String(150))

class Venue(db.Model,UserMixin):
    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(150),unique=True)
    venue_capacity = db.Column(db.String(150), nullable=False)
    venue_rating = db.Column(db.String(150))
    venue_location = db.Column(db.String(150))
    venue_city = db.Column(db.String(150))

class Booking(db.Model,UserMixin):
    booking_id = db.Column(db.Integer, primary_key=True)
    booking_user = db.Column(db.String(150))
    booking_movie_name = db.Column(db.String(150))
    booking_venue = db.Column(db.String(150))
    booking_time = db.Column(db.String(150))
    booking_seats = db.Column(db.Integer)
    booking_cost = db.Column(db.Integer)   
    booking_rateing = db.Column(db.Integer,default=0) 




