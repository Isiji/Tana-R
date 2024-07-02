import logging
from flask import Blueprint, current_app, render_template, request, flash, jsonify, redirect, url_for
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana import db_storage
import pandas as pd
import os
import csv

representation = Blueprint('representation', __name__)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@representation.route('/pollingstations', methods=['GET'])
def view_results():
    constituencies = db_storage.all(Constituency).values()
    wards = db_storage.all(Ward).values()
    polling_stations = db_storage.all(PollingStation).values()
    return render_template('results.html', title='Results', constituencies=constituencies, wards=wards, polling_stations=polling_stations)
