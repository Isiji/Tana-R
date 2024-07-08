#!/usr/bin/python3
"""Users class module for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from Tana.models.roles import UserRole

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

    diaries = relationship("Diary", back_populates="user")
    human_resources = relationship("HumanResource", uselist=False, back_populates="user")
    tasks_assigned = relationship("Tasks", back_populates="assigned_by_user", foreign_keys="Tasks.assigned_by")
    tasks_assigned_to = relationship("Tasks", back_populates="assigned_to_user", foreign_keys="Tasks.assigned_to")
    reminders = relationship("Reminder", back_populates="user")
    offices = relationship("Offices", back_populates="users")
    events = relationship("Events", back_populates="user")
    # Removed the employee_registers relationship

    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of a user"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    @staticmethod
    def get_user_by_email(email):
        """get a user by email"""
        return users.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(id):
        """get a user by id"""
        return users.query.filter_by(id=id).first()

    def has_role(self, role):
        """check if a user has a role"""
        return self.role == role

    @staticmethod
    def create_user(name, email, password, phone, ID_No, role, office_id):
        """creates a user"""
        from Tana import db_storage

        if role not in UserRole._value2member_map_:
            raise ValueError("Invalid role")

        user = users(
            name=name,
            email=email,
            password=password,
            phone=phone,
            ID_No=ID_No,
            role=role,
            office_id=office_id,
        )

        db_storage.new(user)
        db_storage.save()
        return user

    @staticmethod
    def create_super_admin():
        """creates a superadmin user"""
        from Tana import db_storage, bcrypt
        password_hash = bcrypt.generate_password_hash("password").decode('utf-8')
        super_admin = users(
            name="Ziggy",
            email="ziggy@gmail.com",
            password=password_hash,
            phone=1234,
            ID_No=1234,
            role=UserRole.SUPER_ADMIN.value,
            office_id=None,
        )

        db_storage.new(super_admin)
        db_storage.save()
        return super_admin

    def can_register_user(self, role):
        """checks if the current user can register a user"""
        allowed_roles = {
            UserRole.SUPER_ADMIN: [
                UserRole.ADMIN, UserRole.DRIVER, UserRole.MANAGER, UserRole.BODYGUARD,
                UserRole.RESEARCHER, UserRole.SECRETARY, UserRole.CHIEF_FIELD_OFFICER,
                UserRole.CHIEF_SECURITY_OFFICER, UserRole.COORDINATOR, UserRole.FIELD_OFFICER,
                UserRole.P_A
            ],
            UserRole.ADMIN: [UserRole.P_A, UserRole.DRIVER, UserRole.BODYGUARD, UserRole.RESEARCHER, UserRole.COORDINATOR, UserRole.SECRETARY, UserRole.CHIEF_SECURITY_OFFICER, UserRole.CHIEF_FIELD_OFFICER, UserRole.FIELD_OFFICER],
            UserRole.P_A: [UserRole.DRIVER, UserRole.BODYGUARD, UserRole.RESEARCHER, UserRole.COORDINATOR, UserRole.SECRETARY, UserRole.CHIEF_SECURITY_OFFICER, UserRole.CHIEF_FIELD_OFFICER, UserRole.FIELD_OFFICER]
        }
        return role in allowed_roles.get(self.role, [])
