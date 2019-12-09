import json
from db import db, User, Trip, Event, Category
from flask import Flask, request
from flask_migrate import Migrate

db_filename = "travel.db"
app = Flask(__name__)

migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/api/users/')
def get_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    username = post_body.get('username', '')
    bio = post_body.get('bio')
    picture_link = post_body.get('picture_link')
    user = User(
        name = name,
        username = username,
        bio = bio,
        picture_link = picture_link
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/user/<int:user_id>/', methods=['POST'])
def update_user(user_id):
    post_body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    name = post_body.get('name', user.name)
    username = post_body.get('username', user.username)
    bio = post_body.get('bio', user.bio)
    picture_link = post_body.get('picture_link', user.picture_link)
    user.name = name
    user.username = username
    user.bio = bio
    user.picture_link = picture_link
    db.session.commit()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    db.session.delete(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/user/<int:user_id>/trips/')
def get_trips(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trips = user.trips
    res = {'success': True, 'data': [t.serialize() for t in trips]}
    return json.dumps(res), 200

@app.route('/api/user/<int:user_id>/trips/', methods=['POST'])
def create_trip(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    post_body = json.loads(request.data)
    title = post_body.get('title', '')
    picture_link = post_body.get('picture_link')
    start_date = post_body.get('start_date', '')
    end_date = post_body.get('end_date', '')
    location = post_body.get('location', '')
    description = post_body.get('description', '')
    trip = Trip(
        title = title,
        picture_link = picture_link,
        start_date = start_date,
        end_date = end_date,
        location = location,
        description = description,
        user_id = user_id
    )
    user.trips.append(trip)
    db.session.add(trip)
    db.session.commit()
    return json.dumps({'success': True, 'data': trip.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/')
def get_trip(user_id, trip_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    return json.dumps({'success': True, 'data': trip.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/', methods=['POST'])
def update_trip(user_id, trip_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    post_body = json.loads(request.data)
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    title = post_body.get('title', trip.title)
    picture_link = post_body.get('picture_link', trip.picture_link)
    start_date = post_body.get('start_date', trip.start_date)
    end_date = post_body.get('end_date', trip.end_date)
    location = post_body.get('location', trip.location)
    description = post_body.get('description', trip.description)
    trip.title = title
    trip.picture_link = picture_link
    trip.start_date = start_date
    trip.end_date = end_date
    trip.location = location
    trip.description = description
    db.session.commit()
    return json.dumps({'success': True, 'data': trip.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/', methods=['DELETE'])
def delete_trip(user_id, trip_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    db.session.delete(trip)
    db.session.commit()
    return json.dumps({'success': True, 'data': trip.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/events/')
def get_events(user_id, trip_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    events = trip.events
    res = {'success': True, 'data': [e.serialize() for e in events]}
    return json.dumps(res), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/events/', methods=['POST'])
def create_event(user_id, trip_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    date = post_body.get('date', '')
    location = post_body.get('location', '')
    description = post_body.get('description', '')
    event = Event(
        name = name,
        date = date,
        location = location,
        description = description,
        trip_id = trip_id
    )
    trip.events.append(event)
    db.session.add(event)
    db.session.commit()
    return json.dumps({'success': True, 'data': event.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/event/<int:event_id>/')
def get_event(user_id, trip_id, event_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    if ((event in trip.events) == False):
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    return json.dumps({'success': True, 'data': event.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/event/<int:event_id>/', methods=['POST'])
def update_event(user_id, trip_id, event_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    if ((event in trip.events) == False):
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    post_body = json.loads(request.data)
    name = post_body.get('name', event.name)
    date = post_body.get('date', event.date)
    location = post_body.get('location', event.location)
    description = post_body.get('description', event.description)
    event.name = name
    event.date = date
    event.location = location
    event.description = description
    db.session.commit()
    return json.dumps({'success': True, 'data': event.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/event/<int:event_id>/', methods=['DELETE'])
def delete_event(user_id, trip_id, event_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    if ((event in trip.events) == False):
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    db.session.delete(event)
    db.session.commit()
    return json.dumps({'success': True, 'data': event.serialize()}), 200

@app.route('/api/user/<int:user_id>/trip/<int:trip_id>/event/<int:event_id>/category/', methods=['POST'])
def assign_category(user_id, trip_id, event_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    if ((trip in user.trips) == False):
        return json.dumps({'success': False, 'error': 'Trip not found!'}), 404
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    if ((event in trip.events) == False):
        return json.dumps({'success': False, 'error': 'Event not found!'}), 404
    post_body = json.loads(request.data)
    category = Category.query.filter_by(name=post_body.get('name', '')).first()
    if not category:
        category = Category(
            name = post_body.get('name', '')
        )
    event.categories.append(category)
    db.session.add(category)
    db.session.commit()
    return json.dumps({'success': True, 'data': category.serialize()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
