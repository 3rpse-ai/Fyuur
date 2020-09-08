#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from forms import VenueForm, ArtistForm
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
)

venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
)

class Genre(db.Model):
  __tablename__ = 'Genre'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)


def get_genre_choices():
  
  if __name__ == "__main__":
    print("we are doing something")
    genres = Genre.query.all()
    if not genres:

      genre_list=[
                ('Alternative', 'Alternative'),
                ('Blues', 'Blues'),
                ('Classical', 'Classical'),
                ('Country', 'Country'),
                ('Electronic', 'Electronic'),
                ('Folk', 'Folk'),
                ('Funk', 'Funk'),
                ('Hip-Hop', 'Hip-Hop'),
                ('Heavy Metal', 'Heavy Metal'),
                ('Instrumental', 'Instrumental'),
                ('Jazz', 'Jazz'),
                ('Musical Theatre', 'Musical Theatre'),
                ('Pop', 'Pop'),
                ('Punk', 'Punk'),
                ('R&B', 'R&B'),
                ('Reggae', 'Reggae'),
                ('Rock n Roll', 'Rock n Roll'),
                ('Soul', 'Soul'),
                ('Other', 'Other'),
            ]
      
      for genre in genre_list:
        entry = Genre(name=genre[0])
        db.session.add(entry)
      db.session.commit()
      genres = Genre.query.all()


  choices = []
  if __name__ == "__main__":
    for genre in genres:
      choice = (genre.id, genre.name)
      choices.append(choice)
  return choices

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues', lazy=True))
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500), nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    # implemented genre relational table for artists as there is a n:n relationship
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists', lazy=True))
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500), nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []

  cities = db.session.query(Venue.city).group_by(Venue.city).order_by(Venue.city).all()
  state = ""
  for city in cities:
    
    city_states = db.session.query(Venue.state).filter(Venue.city == city[0]).group_by(Venue.state).order_by(Venue.state).all()
    for state in city_states:
      venues = Venue.query.filter(Venue.city == city[0], Venue.state == state[0]).all()
      venue_list = []
      for venue in venues:
        state = venue.state
        venue = {
          "id": venue.id,
          "name": venue.name,
          #TODO add upcoming shows value
          "num_upcoming_shows": 0,
        }
        venue_list.append(venue)
        print(venue_list)

      city_entry = {
        "city": city[0],
        "state": state,
        "venues": venue_list
      }
      data.append(city_entry)
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues = Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  print(venues)
  data = []
  for venue in venues:
    venue_entry = {
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": 0,
    }
    data.append(venue_entry)
  
  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # TODO: input shows from show table, input image & website link
  venue = Venue.query.get(venue_id)
  genres = [genre.name for genre in venue.genres]
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

class VenueGenreForm(VenueForm):
  genres = SelectMultipleField(
        # needed to avoid circular import 
        'genres', validators=[DataRequired()],
        choices=get_genre_choices()
  )

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueGenreForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    genreIds = request.form.getlist('genres')
    genres = []

    for genreId in genreIds:
      genre = Genre.query.get(genreId)
      genres.append(genre)

    seeking_talent = request.form.get('seeking_checkbox')
    seeking_description = request.form.get('seeking_description')

    print(seeking_talent)
    print(seeking_description)

    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False

    if not seeking_talent:
      print("Not seeking talent")
      seeking_description = None
    

    

    new_venue = Venue(
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    address=request.form.get('address'),
    genres=genres,
    phone=request.form.get('phone'),
    image_link=request.form.get('image_link'),
    facebook_link=request.form.get('facebook_link'),
    website=request.form.get('website_link'),
    seeking_talent = seeking_talent,
    seeking_description = seeking_description
    )
    db.session.add(new_venue)
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    
  finally:
    db.session.commit()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  success = False
  try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        success = True
  except:
        db.session.rollback()
  finally:
        db.session.close()
  return jsonify({'success' : success})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  artists = Artist.query.order_by(Artist.name).all()
  for artist in artists:
    entry = {
      "id": artist.id,
      "name": artist.name
    }
    data.append(entry)
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  artists = Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  data = []
  for artist in artists:
    artist_entry = {
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": 0,
    }
    data.append(artist_entry)
  
  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  genres = [genre.name for genre in artist.genres]
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_talent,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
      "artist_id": 4,
      "venue_name": "Guns N Petals",
      "venue_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistGenreForm()
  artist = Artist.query.get(artist_id)

  genres = [str(x.id) for x in artist.genres]

  form.name.data = artist.name
  form.city.data = artist.city
  form.phone.data = artist.phone
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website
  form.image_link.data = artist.image_link
  form.genres.data = genres
  form.seeking_checkbox.data = artist.seeking_talent
  if artist.seeking_talent:
    form.seeking_description.data = artist.seeking_description
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    genreIds = request.form.getlist('genres')
    genres = []

    for genreId in genreIds:
      genre = Genre.query.get(genreId)
      genres.append(genre)

    seeking_talent = request.form.get('seeking_checkbox')
    seeking_description = request.form.get('seeking_description')

    if seeking_talent == 'y':
        seeking_talent = True
    else:
      seeking_talent = False

    if not seeking_talent:
      seeking_description = None

    artist = Artist.query.get(artist_id)
    artist.name=request.form.get('name')
    artist.city=request.form.get('city')
    artist.state=request.form.get('state')
    artist.genres=genres
    artist.phone=request.form.get('phone')
    artist.image_link=request.form.get('image_link')
    artist.facebook_link=request.form.get('facebook_link')
    artist.website=request.form.get('website_link')
    artist.seeking_talent = seeking_talent
    artist.seeking_description = seeking_description
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be updated.')
    
  finally:
    db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueGenreForm()
  venue = Venue.query.get(venue_id)

  genres = [str(x.id) for x in venue.genres]

  form.name.data = venue.name
  form.city.data = venue.city
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website
  form.image_link.data = venue.image_link
  form.genres.data = genres
  form.seeking_checkbox.data = venue.seeking_talent
  if venue.seeking_talent:
    form.seeking_description.data = venue.seeking_description
    
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
    genreIds = request.form.getlist('genres')
    genres = []

    for genreId in genreIds:
      genre = Genre.query.get(genreId)
      genres.append(genre)

    seeking_talent = request.form.get('seeking_checkbox')
    seeking_description = request.form.get('seeking_description')

    if seeking_talent == 'y':
        seeking_talent = True
    else:
      seeking_talent = False

    if not seeking_talent:
      seeking_description = None

    venue = Venue.query.get(venue_id)
    venue.name=request.form.get('name')
    venue.city=request.form.get('city')
    venue.state=request.form.get('state')
    venue.address=request.form.get('address')
    venue.genres=genres
    venue.phone=request.form.get('phone')
    venue.image_link=request.form.get('image_link')
    venue.facebook_link=request.form.get('facebook_link')
    venue.website=request.form.get('website_link')
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be updated.')
    
  finally:
    db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

class ArtistGenreForm(ArtistForm):
  genres = SelectMultipleField(
        # needed to avoid circular import 
        'genres', validators=[DataRequired()],
        choices=get_genre_choices()
  )

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistGenreForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    genreIds = request.form.getlist('genres')
    genres = []

    for genreId in genreIds:
      genre = Genre.query.get(genreId)
      genres.append(genre)

    seeking_talent = request.form.get('seeking_checkbox')
    seeking_description = request.form.get('seeking_description')

    print(seeking_talent)
    print(seeking_description)

    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False

    if not seeking_talent:
      print("Not seeking talent")
      seeking_description = None
    

    

    new_artist = Artist(
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    genres=genres,
    phone=request.form.get('phone'),
    image_link=request.form.get('image_link'),
    facebook_link=request.form.get('facebook_link'),
    website=request.form.get('website_link'),
    seeking_talent = seeking_talent,
    seeking_description = seeking_description
    )
    db.session.add(new_artist)
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    
  finally:
    db.session.commit()

  return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  success = False
  try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        success = True
  except:
        db.session.rollback()
  finally:
        db.session.close()
  return jsonify({'success' : success})


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
