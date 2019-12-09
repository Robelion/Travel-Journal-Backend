from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    picture_link = db.Column(db.String)
    trips = db.relationship('Trip', cascade='delete')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.username = kwargs.get('username', '')
        self.bio = kwargs.get('bio')
        self.picture_link = kwargs.get('picture_link')
        self.trips = []

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'bio': self.bio,
            'picture_link': self.picture_link,
            'trips': [t.serialize() for t in self.trips]
        }

class Trip(db.Model):
    __tablename__ = 'trip'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    picture_link = db.Column(db.String)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    events = db.relationship('Event', cascade='delete')


    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.picture_link = kwargs.get('picture_link')
        self.start_date = kwargs.get('start_date', '')
        self.end_date = kwargs.get('end_date', '')
        self.location = kwargs.get('location', '')
        self.description = kwargs.get('description', '')
        self.events = []

    def serialize(self):
        return{
            'id': self.id,
            'title': self.title,
            'picture_link': self.picture_link,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'location': self.location,
            'description': self.description,
            'events': [e.serialize() for e in self.events]
        }

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    categories = db.relationship('Category', secondary=association_table, back_populates='events')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.date = kwargs.get('date', '')
        self.location = kwargs.get('location', '')
        self.description = kwargs.get('description', '')

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'location': self.location,
            'description': self.description,
            'categories': [c.serialize() for c in self.categories]
        }

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    events = db.relationship('Event', secondary=association_table, back_populates='categories')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }
