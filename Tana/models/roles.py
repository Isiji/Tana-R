#!/usr/bin/python3
"""Roles class for the roles"""

from enum import Enum as PyEnum

class UserRole(PyEnum):
    """This class defines the user roles"""
    ADMIN = "admin"
    DRIVER = "driver"
    BODYGUARD = "bodyguard"
    RESEACHER = "researcher"
    COORDINATOR = "coordinator"
    