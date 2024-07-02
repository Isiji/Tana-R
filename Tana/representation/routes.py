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


@representation.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@representation.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file_path = current_app.config['CSV_FILE_PATH']
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Log the fieldnames to debug the CSV structure
            fieldnames = reader.fieldnames
            print(f"CSV Fieldnames: {fieldnames}")

            for row in reader:
                constituency_name = row['constituency']
                ward_name = row['ward']
                polling_station_name = row['polling_station']

                constituency, created = db_storage.get_or_create(Constituency, defaults={'name': constituency_name}, name=constituency_name)
                ward, created = db_storage.get_or_create(Ward, defaults={'name': ward_name, 'constituency_id': constituency.id}, name=ward_name, constituency_id=constituency.id)
                polling_station, created = db_storage.get_or_create(PollingStation, defaults={'name': polling_station_name, 'ward_id': ward.id}, name=polling_station_name, ward_id=ward.id)
                
                db_storage.save()

        return "CSV data has been uploaded and saved to the database."
    except Exception as e:
        return f"An error occurred: {e}"