#!/usr/bin/python3
"""users class module for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Boolean, String, Integer, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from flask_login import UserMixin
from Tana.models.roles import UserRole
import hashlib

class users(BaseModel, Base, UserMixin):
    """This class defines the users model"""
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False)
    ID_No = Column(Integer, nullable=False)
    role = Column(String(128), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=True)
    is_active = Column(Boolean, default=True)

    diaries = relationship("Diary", back_populates="user")
    human_resources = relationship("HumanResource", uselist=False, back_populates="user")
    tasks_assigned = relationship("Tasks", back_populates="assigned_by_user", foreign_keys="Tasks.assigned_by")
    tasks_assigned_to = relationship("Tasks", back_populates="assigned_to_user", foreign_keys="Tasks.assigned_to")
    reminders = relationship("Reminder", back_populates="user")
    offices = relationship("Offices", back_populates="users")

    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def get_user_by_email(self, email):
        """get a user by email"""
        return self.query.filter_by(email=email).first()
    
    def get_user_by_id(self, id):
        """get a user by id"""
        return self.query.filter_by(id=id).first()
    
    def has_role(self, role):
        """check if a user has a role"""
        return self.role == role
    
    @staticmethod
    def create_user(name, email, password, phone, ID_No, role, office_id):
        """creates a user"""
        from Tana import db_storage

        if role not in [UserRole.ADMIN.value, UserRole.DRIVER.value, UserRole.MANAGER.value, UserRole.BODYGUARD.value, UserRole.RESEARCHER.value, UserRole.SECRETARY.value, UserRole.CHIEF_FIELD_OFFICER.value, UserRole.CHIEF_SECURITY_OFFICER.value, UserRole.COORDINATOR.value, UserRole.FIELD_OFFICER.value]:
            raise ValueError("Invalid role")
        
        user = users(
            name=name,
            email=email,
            password=password,
            phone=phone,
            ID_No=ID_No,
            role=role,
            office_id=office_id,
            is_active=True
            )
        
        db_storage.new(user)
        db_storage.save()
        return user
    @staticmethod
    def create_super_admin():
        """creates a superadmin user"""
        from Tana import db_storage
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        super_admin = users(
            name="Ziggy",
            email="ziggy@gmail.com",
            password=password_hash,
            phone=1234,
            ID_No=1234,
            role=UserRole.SUPER_ADMIN.value,
            office_id=None,
            is_active=True
            )
        
        db_storage.new(super_admin)
        db_storage.save()
        return super_admin
    
    def can_register_user(self, role):
        """checks if the current user can register a user"""
        if self.has_role(UserRole.SUPER_ADMIN.value):
            return role in [UserRole.ADMIN.value, UserRole.DRIVER.value, UserRole.MANAGER.value, UserRole.BODYGUARD.value, UserRole.RESEARCHER.value, UserRole.SECRETARY.value, UserRole.CHIEF_FIELD_OFFICER.value, UserRole.CHIEF_SECURITY_OFFICER.value, UserRole.COORDINATOR.value, UserRole.FIELD_OFFICER.value]
        elif self.has_role(UserRole.ADMIN.value):
            return role == UserRole.USER.value
        return False