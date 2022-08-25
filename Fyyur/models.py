from tkinter import CASCADE
from . import db

Artist_Genre = db.Table(
    "Artist_Genres",
    db.metadata,
    db.Column("artist_id", db.ForeignKey("Artists.id"), primary_key=True),
    db.Column("genre_id", db.ForeignKey("Genres.id"), primary_key=True),
)

Venue_Genre = db.Table(
    "Venue_Genres",
    db.metadata,
    db.Column("venue_id", db.ForeignKey("Venues.id"), primary_key=True),
    db.Column("genre_id", db.ForeignKey("Genres.id"), primary_key=True),
)
class Show(db.Model):
    __tablename__ = "Shows"
    venue_id = db.Column(db.Integer,db.ForeignKey("Venues.id", ondelete="CASCADE"), primary_key=True)
    artist_id = db.Column(db.Integer,db.ForeignKey("Artists.id", ondelete="CASCADE"), primary_key=True)
    start_date = db.Column(db.DateTime, primary_key = True)
    venue = db.relationship('Venue',back_populates="shows")
    artist = db.relationship('Artist',back_populates="shows")
    

class Venue(db.Model):
    __tablename__ = 'Venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship("Show", back_populates="venue", cascade="all, delete")
    genres = db.relationship("Genre", secondary=Venue_Genre, back_populates="venues")
    

    def get_venues():
        return Venue.query.all()

Venue.get_venues = staticmethod(Venue.get_venues)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(1000))
    seeking_venue = db.Column(db.Boolean())
    shows = db.relationship("Show", back_populates="artist", cascade="all, delete")
    genres = db.relationship("Genre", secondary=Artist_Genre, back_populates="artists")

    def get_artists():
        return Artist.query.all()

Artist.get_artist = staticmethod(Artist.get_artists)

class Genre(db.Model):
    __tablename__ = 'Genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artists = db.relationship(
        "Artist", secondary=Artist_Genre, back_populates="genres")
    venues = db.relationship(
        "Venue", secondary=Venue_Genre, back_populates="genres")
    
    def get_genres():
       return Genre.query.all()

Genre.get_genres = staticmethod(Genre.get_genres)