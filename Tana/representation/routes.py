# Tana/representation/routes.py
import logging
from flask import Blueprint, current_app, render_template, request, jsonify
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana import db_storage

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
def pollingstations():
    constituencies = db_storage.all(Constituency).values()
    wards = db_storage.all(Ward).values()
    polling_stations = db_storage.all(PollingStation).values()
    return render_template('results.html', title='Results', constituencies=constituencies, wards=wards, polling_stations=polling_stations)

@representation.route('/select_polling_station', methods=['GET'])
def select_polling_station():
    return render_template('select_polling_station.html')

@representation.route('/get_all_polling_stations', methods=['GET'])
def get_all_polling_stations():
    current_app.logger.info('Fetching all polling stations')
    try:
        polling_stations = db_storage.all(PollingStation)
        current_app.logger.info('Polling stations fetched: %s', polling_stations)
        polling_station_list = [ps.name for ps in polling_stations.values()]
        return jsonify({'pollingStations': polling_station_list})
    except Exception as e:
        current_app.logger.error('Error fetching polling stations: %s', e)
        return jsonify({"error": str(e)}), 500

@representation.route('/get_polling_station_info', methods=['GET'])
def get_polling_station_info():
    polling_station_name = request.args.get('polling_station')
    logging.debug(f"Received request for /get_polling_station_info with polling_station={polling_station_name}")
    polling_station = db_storage.get_pollingstation_by_name(polling_station_name)
    
    if polling_station:
        ward = db_storage.get_ward_by_id(polling_station.ward_id)
        constituency = db_storage.get_constituency_by_id(ward.constituency_id) if ward else None
        logging.debug(f"Fetched ward: {ward.name if ward else 'None'}, constituency: {constituency.name if constituency else 'None'}")
        return jsonify({
            'ward': ward.name if ward else None,
            'constituency': constituency.name if constituency else None
        })
    else:
        logging.debug("Polling station not found")
        return jsonify({'error': 'Polling station not found'}), 404
    

@representation.route('/pollingstations_list', methods=['GET'])
def pollingstations_list():
    polling_stations = db_storage.all(PollingStation)
    polling_station_names = [ps.name for ps in polling_stations]
    return jsonify(polling_station_names)

@representation.route('/pollingstations/<polling_station_name>', methods=['GET'])
def get_polling_station_details_by_name(polling_station_name):
    polling_station = db_storage.get_polling_station_by_name(polling_station_name)
    if polling_station:
        return jsonify({
            'ward': polling_station.ward.name,
            'constituency': polling_station.constituency.name
        })
    else:
        return jsonify({'error': 'Polling station not found'}), 404