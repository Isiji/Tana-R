#!/usr/bin/python3
"""config file for the app"""
import os

class Config:
    """Config class for the app"""
    SECRET_KEY = "Tana"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://Tana:Tana123.@localhost/Tana'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FILE_PATH = os.path.join(os.getcwd(), 'Tana', 'representation', 'tanawards.csv')
