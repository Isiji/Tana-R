#!/usr/bin/python3
"""Database storage module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sys
from sqlalchemy.exc import SQLAlchemyError
from Tana.models.base_model import Base
from Tana.models.members import users
from Tana.models.functions import FunctionCategory
from Tana.models.roles import UserRole
from Tana.models.offices import Offices
from Tana.models.reminder import Reminder
from Tana.models.tasks import Tasks
from Tana.models.attendees import Attendees
from Tana.models.diary import Diary
from Tana.models.commitments import Commitments
from Tana.models.calendarEvents import CalendarEvents
from Tana.models.contributions import Contributions
from Tana.models.functions import Functions
from Tana.models.humanresource import HumanResource

class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self,  app=None):
        """Initializes the database storage"""
        if app is not None:
            self.__engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)
        else:
            self.__engine = create_engine('mysql+mysqldb://Tana:Tana123.@localhost/Tana', pool_pre_ping=True)
        
        if 'test' in sys.argv:
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        objects = {}
        try:
            if cls is not None:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(cls.__name__, obj.id)
                    objects[key] = obj
            else:
                classes = [users, FunctionCategory, UserRole, Offices, Reminder, Tasks, Attendees, Diary, Commitments, CalendarEvents, Contributions, Functions, HumanResource]
                for cls in classes:
                    query_result = self.__session.query(cls).all()
                    for obj in query_result:
                        key = "{}.{}".format(cls.__name__, obj.id)
                        objects[key] = obj
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
        return objects

    
    def new(self, obj):
        """Adds the object to the current database session"""
        try:
            self.__session.add(obj)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def save(self):
        """Commits all changes to the database"""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            print("An Error Occured:", e)
    
    def get_user(self, user):
        """Returns the user object"""
        try:
            query_result = self.__session.query(users).filter_by(email=user).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_office(self, office):
        """Returns the office object"""
        try:
            query_result = self.__session.query(Offices).filter_by(office_name=office).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)
    def get(self, cls, **kwargs):
        """Returns the object based on the class and keyword arguments"""
        try:
            query_result = self.__session.query(cls).filter_by(**kwargs).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def delete(self, obj=None):
        """Deletes the object from the current database session"""
        try:
            if obj:
                self.__session.delete(obj)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def reload(self):
        """Creates all tables in the database"""
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine)
            self.__session = scoped_session(session_factory)
            self.__session.configure(bind=self.__engine)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)


    def close(self):
        """Closes the current session"""
        try:    
            self.__session.remove()
            self.__session.close()
        except SQLAlchemyError as e:
            print("An Error Occured:", e)