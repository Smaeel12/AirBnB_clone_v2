#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey(
        'cities.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(60), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer(), nullable=False, default=0)
    number_bathrooms = Column(Integer(), nullable=False, default=0)
    max_guest = Column(Integer(), nullable=False, default=0)
    price_by_night = Column(Integer(), nullable=False, default=0)
    latitude = Column(Float(), nullable=True)
    longitude = Column(Float(), nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review',
                               backref=backref("place", cascade="all,delete"),
                               cascade='all, delete',
                               passive_deletes=True)
        amenities = relationship('Amenity',
                                 secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            return [obj for obj in storage.all(Review).values()
                    if obj.place_id == self.id]

        @property
        def amenities(self):
            from models import storage
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            if obj.__class__.__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
