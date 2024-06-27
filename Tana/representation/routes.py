from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana import db_storage  # Adjusted import
import pandas as pd
import os
from werkzeug.utils import secure_filename

representation = Blueprint('representation', __name__)

@representation.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                process_csv_file(file_path)  # Call process_csv_file without arguments
                flash('File successfully uploaded and processed', 'success')
                return redirect(url_for('representation.upload_file'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
                return redirect(request.url)
    return render_template('upload.html')

@representation.route('/autofill', methods=['POST', 'GET'])
def autofill():
    if request.method == 'POST':
        polling_station_name = request.form.get('polling_station')
        result = autofill_polling_station(polling_station_name)
        if result:
            return render_template('autofill.html', result=result)
        else:
            flash('Polling Station not found', 'danger')
            return render_template('autofill.html')
    return render_template('autofill.html')

@representation.route('/process_csv')
def process_csv():
    file_path = os.path.join(current_app.config['BASE_DIR'], 'representation', 'tanawards.csv')
    try:
        process_csv_file(file_path)  # Call your processing function here
        flash('CSV file processed successfully', 'success')
    except Exception as e:
        flash(f'An error occurred while processing CSV: {str(e)}', 'danger')
    return redirect(url_for('representation.autofill'))  # Redirect to appropriate page

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

def process_csv_file(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        constituency_name = row['constituency']
        ward_name = row['ward']
        polling_station_name = row['polling_station']

        # Ensure names are strings
        constituency_name = str(constituency_name)
        ward_name = str(ward_name)
        polling_station_name = str(polling_station_name)

        print(f"Processing CSV row: Constituency={constituency_name}, Ward={ward_name}, Polling Station={polling_station_name}")

        constituency = db_storage.get(Constituency, name=constituency_name)
        if not constituency:
            constituency = Constituency(name=constituency_name)
            db_storage.new(constituency)
            db_storage.save()

        ward = db_storage.get(Ward, name=ward_name, constituency_id=constituency.id)
        if not ward:
            ward = Ward(name=ward_name, constituency_id=constituency.id)
            db_storage.new(ward)
            db_storage.save()

        polling_station = db_storage.get(PollingStation, name=polling_station_name, ward_id=ward.id)
        if not polling_station:
            polling_station = PollingStation(name=polling_station_name, ward_id=ward.id)
            db_storage.new(polling_station)
            db_storage.save()

def autofill_polling_station(polling_station_name):
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
