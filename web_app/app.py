from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_wtf import FlaskForm
# from wtforms import TextField, BooleanField
from datetime import datetime, timedelta
from utils import describe_data, bytes_to_wavfile, DataRequestForm, default_start, default_end

from flask_cors import CORS

import os

app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'our very hard to guess secretfir'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route('/')
def index():
    return redirect(url_for('data_request'))


@app.route('/data_request', methods=['GET', 'POST'])
def data_request():
    form = DataRequestForm(request.form)

    if request.method == 'POST':
        input_ticker = form.input_ticker.data
        input_start_date = form.input_start_date.data
        input_end_date = form.input_end_date.data
        input_interval = form.input_interval.data
        download = form.download.data
        generate_chart = form.generate_chart.data

        try:
            d = describe_data(input_ticker, input_start_date, input_end_date, input_interval, download)
            data_frame = d.get_data()

            if generate_chart:
                labels = list(data_frame['date_time'])
                values = list(data_frame['Adj Close'])
                return render_template('chart.html', dates=labels, adj_close=values)
        except:
            print('error aa rela hai')
            return redirect(url_for('data_request'))

    return render_template('requestForm.html', default_start=default_start, default_end=default_end)




@app.route('/recorder')
def recorder():
    return render_template('speechRecorder.html')


@app.route("/audioUpload", methods=['POST'])
def audio_upload():
    if request.method == 'POST':
        bytes_to_wavfile(request.data)
    return "saved file to disk."



if __name__ == "__main__":
    # Run the application
    app.run(debug=True)