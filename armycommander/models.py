from sqlalchemy import (
    Column,
    Index,
    Integer,
    ForeignKey,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from pyramid.security import (
Allow,
Everyone,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key = True)
    name = Column(Text, primary_key=True)

    def __repr__(self):
        return self.name



class Map(Base):
    __tablename__ = 'map'
    id = Column(Integer, primary_key = True)
    name = Column(Text, primary_key = True)
    ratings = relationship("TopRating", backref = 'map', lazy='dynamic')    
    def __repr__(self):
        return self.name

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key = True)
    value = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('player.id'))
    #user = relationship("Player", backref = 'score')
    map_id = Column(Integer, ForeignKey('map.id'))
    #map_ = relationship("Map", backref='score')

    def __repr__(self):
        return self.value



class TopRating(Base):
    __tablename__ = 'top_rating'
    id = Column(Integer, primary_key = True)    
    map_id = Column(Integer, ForeignKey('map.id'))
    first_user_name = Column(Text, ForeignKey('player.name'))
    second_user_name = Column(Text, ForeignKey('player.name'))
    third_user_name = Column(Text, ForeignKey('player.name'))

    def __repr__(self):
        return self.first_user_name + ' ' + self.second_user_name + ' ' + self.third_user_name


class AccessGroups(object):
    	__name__ = None
	__acl__ = [
	(Allow, 'group:editors', 'edit'),       
	(Allow, Everyone, 'view'),
	    ]
	def __init__(self, request):
        	pass


