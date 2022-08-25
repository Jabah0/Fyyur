from ast import main
from crypt import methods
import json
from tkinter import CASCADE
import dateutil.parser
import babel
from flask import Flask, Blueprint, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from Fyyur.forms import *
from markupsafe import Markup
from flask_migrate import Migrate
import sys
from datetime import date
from . import db
from Fyyur.models import *


apps = Blueprint('apps', __name__)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
@apps.app_template_filter()
def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@apps.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@apps.route('/venues')
def venues():
  #  [DONE] TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  areas=Venue.query.with_entities(Venue.city,Venue.state).distinct()
  #venues= Venue.query().all()
  venues=Venue.query.all()
  return render_template('pages/venues.html', areas=areas, venues=venues);

@apps.route('/venues/search', methods=['POST'])
def search_venues():
  # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search = "%{}%".format(request.form.get('search_term', ''))
  results = Venue.query.filter(Venue.name.ilike(search))
  count = results.count()
  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''),count=count)

@apps.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # [DONE]  shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  now = datetime.now()
  venue=Venue.query.get(venue_id)

  upcoming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_date > now).all()
  upcoming_shows_count = len(upcoming_shows)

  past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_date < now).all()
  past_shows_count = len(past_shows)
  
  return render_template('pages/show_venue.html', venue=venue,past_shows=past_shows, upcoming_shows=upcoming_shows, past_shows_count=past_shows_count, upcoming_shows_count=upcoming_shows_count)

#  Create Venue
#  ----------------------------------------------------------------

@apps.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@apps.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # [DONE] TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  error = False
  try:
      
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data

    venue = Venue(name=name,city=city,state=state,phone=phone,address=address,
                    image_link=image_link,facebook_link=facebook_link,seeking_description=seeking_description,
                    seeking_talent=seeking_talent)
    db.session.add(venue)
    db.session.commit()
  except:
        error = True
        db.session.rollback()
        error = True
        print(sys.exc_info())
  finally:
        db.session.close()

  # on successful db insert, flash success
  if (not error):
  # on successful db insert, flash success
      flash('Venue ' + name + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
      flash('An error occurred. Venue ' + name + ' could not be listed.')

  return render_template('pages/home.html')

@apps.route('/venues/<int:venue_id>', methods=["DELETE"])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  finally:
    db.session.close()  
  # [DONE] BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('apps.index'))

#  Artists
#  ----------------------------------------------------------------
@apps.route('/artists')
def artists():
  # [DONE] TODO: replace with real data returned from querying the database
  
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)

@apps.route('/artists/search', methods=['POST'])
def search_artists():
  # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search = "%{}%".format(request.form.get('search_term', ''))
  results = Artist.query.filter(Artist.name.ilike(search))
  count = results.count()
  
  return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''), count=count)

@apps.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # [DONE]  TODO: replace with real artist data from the artist table, using artist_id
  now = datetime.now()
  upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_date > now).all()
  upcoming_shows_count= len(upcoming_shows)
  past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_date < now).all()
  past_shows_count = len(past_shows)
  artist = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows, past_shows=past_shows,
                          upcoming_shows_count=upcoming_shows_count, past_shows_count=past_shows_count)

@apps.route('/artists/addTime/<int:artist_id>')                          

#  Update
#  ----------------------------------------------------------------
@apps.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # [DONE] TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@apps.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # [DONE] TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)
  error = False
  try:
      
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_description = form.seeking_description.data
      artist.seeking_venue = form.seeking_venue.data
      artist.genres.clear()
      for genre in form.genres.data:
            artist.genres.append(Genre.query.get(genre.id))
      

      db.session.commit()

      flash('The Artist was successfully updated!')
  except:
      error = True
      db.session.rollback()
      error = True
      print(sys.exc_info())
      flash('An error occurred. The Artist could not be updated.')
  finally:
      db.session.close()

  return redirect(url_for('apps.show_artist', artist_id=artist_id))

@apps.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # [DONE] TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@apps.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # [DONE] TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)
  error = False
  try:
      
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.addres = form.address.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.seeking_description = form.seeking_description.data
      venue.seeking_talent = form.seeking_talent.data
      venue.genres.clear()
      for genre in form.genres.data:
            venue.genres.append(Genre.query.get(genre.id))

      db.session.commit()

      flash('The Venue was successfully updated!')
  except:
      error = True
      db.session.rollback()
      error = True
      print(sys.exc_info())
      flash('An error occurred. The Venue could not be updated.')
  finally:
      db.session.close()

  return redirect(url_for('apps.show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@apps.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@apps.route('/artists/create', methods=['POST'])
def create_artist_submission():
  #[[DONE]]
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    error = False
    try:
        
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        seeking_venue = form.seeking_venue.data
        seeking_description = form.seeking_description.data

        artist = Artist(name=name,city=city,state=state,phone=phone,
                        image_link=image_link,facebook_link=facebook_link,
                        seeking_description=seeking_description,seeking_venue=seeking_venue)
        for genre in form.genres.data:
            artist.genres.append(Genre.query.get(genre.id))            
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

  # on successful db insert, flash success
    if (not error):
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else : 
    # [DONE]TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' +  name + ' could not be listed.')
    return render_template('pages/home.html')

@apps.route('/artists/<int:artist_id>', methods=["DELETE"])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
  finally:
    db.session.close()  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('apps.index'))    


#  Shows
#  ----------------------------------------------------------------

@apps.route('/shows')
def shows():
  # displays list of shows at /shows
  #[DONE] TODO: replace with real venues data.
  shows = Show.query.all()
  return render_template('pages/shows.html', shows=shows)

@apps.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@apps.route('/shows/create', methods=['POST'])
def create_show_submission():
  # [DONE] called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    form = ShowForm(request.form)
    show = Show(artist_id = int(form.artist_id.data.id), venue_id = int(form.venue_id.data.id), start_date=form.start_time.data)
    db.session.add(show)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()  
  return render_template('pages/home.html')


@apps.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@apps.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
