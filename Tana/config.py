#!/usr/bin/python3
"""config file for the app"""
import os

class Config:
    """Config class for the app"""
    SECRET_KEY = "Tana"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://Tana:Tana123.@localhost/Tana'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FILE_PATH = os.path.join(os.getcwd(), 'Tana', 'representation', 'tanawards.csv')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'blairisiji@gmail.com'  # Replace with your actual email
    MAIL_PASSWORD = 'ndny npyi gemz fycj'  # Replace with your actual email password
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'  # Replace with your default sender email