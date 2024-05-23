#!/usr/bin/env python3
"""Users route for the users"""


from flask import Blueprint
from Tana.models.users import users

users = Blueprint('users', __name__)

#create route for admin to register users to the database and assign them roles
@users.route('/register', methods=['POST'])
def register():
    """This function registers a user"""
    pass
    
    

