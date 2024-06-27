import logging
from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for, jsonify
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana import db_storage
import pandas as pd
import os

representation = Blueprint('representation', __name__)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@representation.route('/read_csv', methods=['GET'])
def read_csv():
    try:
        polling_stations = db_storage.all(PollingStation)
        print(f"Polling Stations: {polling_stations}")
        return render_template('select_polling_station.html', polling_stations=polling_stations)
    except Exception as e:
        logger.exception('Error retrieving polling stations: %s', e)
        flash('Error retrieving polling stations', 'danger')
        return render_template('error.html', error=str(e))


@representation.route('/autofill', methods=['POST'])
def autofill():
    try:
        polling_station_name = request.form.get('polling_station')
        result = autofill_polling_station(polling_station_name)
        if result:
            return render_template('autofill.html', result=result)
        else:
            flash('Polling Station not found', 'danger')
            return render_template('autofill.html')
    except Exception as e:
        flash(f'An error occurred during autofill: {str(e)}', 'danger')
        logger.exception('Error during autofill: %s', e)  # Log the exception
        return render_template('autofill.html')

@representation.route('/process_csv')
def process_csv():
    try:
        process_csv_file()  # Call your processing function here
        flash('CSV file processed successfully', 'success')
    except Exception as e:
        flash(f'An error occurred while processing CSV: {str(e)}', 'danger')
        logger.exception('Error processing CSV: %s', e)  # Log the exception
    return redirect(url_for('representation.autofill'))  # Redirect to appropriate page

@representation.route('/pollingstations', methods=['GET'])
def get_polling_stations():
    print('getting polling stations')
    polling_stations = db_storage.all('PollingStation')
    result = []
    for key, station in polling_stations.items():
        result.append({
            'id': station.id,
            'name': station.name,
            'ward_id': station.ward_id,
            'constituency_id': station.constituency_id
        })
    return jsonify(result)   
@representation.route('/polling_station_details/<string:polling_station_name>', methods=['GET'])
def get_polling_station_details_by_name(polling_station_name):
    """Route to fetch the details of a specific polling station"""
    polling_station = db_storage.get(PollingStation, name=polling_station_name)
    if polling_station:
        details = {
            'ward': polling_station.ward.name,
            'constituency': polling_station.constituency.name
        }
        return jsonify(details)
    else:
        return jsonify({'error': 'Polling station not found'}), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

def process_csv_file():
    try:
        file_path = os.path.join(current_app.config['BASE_DIR'], 'representation', 'tanawards.csv')
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            constituency_name = row['constituency']
            ward_name = row['ward']
            polling_station_name = row['polling_station']

            constituency, _ = db_storage.get_or_create(Constituency, name=constituency_name)
            ward, _ = db_storage.get_or_create(Ward, name=ward_name, constituency_id=constituency.id)
            db_storage.new(PollingStation(name=polling_station_name, ward_id=ward.id))
        
        db_storage.save()
    except Exception as e:
        logger.exception('Error processing CSV: %s', e)  # Log the exception

def autofill_polling_station(polling_station_name):
    try:
        polling_station = db_storage.get(PollingStation, name=polling_station_name)
        if polling_station:
            ward = db_storage.get(Ward, id=polling_station.ward_id)
            constituency = db_storage.get(Constituency, id=ward.constituency_id)
            return {
                'Polling Station': polling_station.name,
                'Ward': ward.name,
                'Constituency': constituency.name
            }
        return None
    except Exception as e:
        logger.exception('Error autofilling polling station: %s', e)  # Log the exception
        return None

@representation.route('/pollingstations_list', methods=['GET'])
def get_pollingstations_list():
    """Route to fetch the list of polling station names"""
    try:
        polling_stations = db_storage.all(PollingStation)  # Fetch all polling stations from the database
        print(f"Polling stations fetched: {polling_stations}")  # Debug statement to check the data
        if not polling_stations:
            return jsonify([])  # Return an empty list if no polling stations are found
        polling_station_names = [station.name for station in polling_stations.values()]
        return jsonify(polling_station_names)
    except Exception as e:
        # Log the exception if there's an error
        logging.error(f"Error fetching polling stations: {e}")
        return jsonify([]), 500