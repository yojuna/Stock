from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from datetime import datetime, timedelta
from utils import describe_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


default_start = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day-1)
default_end = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')


# More powerful approach using WTForms
class RegistrationForm(FlaskForm):
    input_ticker = TextField('Ticker', default = 'TATAMOTORS.NS')
    input_start_date = TextField('Start Date', default = default_start)
    input_end_date = TextField('End Date', default=default_end)
    input_interval = TextField('Interval', default='5m')
    download = BooleanField('Download Data')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        input_ticker = form.input_ticker.data
        input_start_date = form.input_start_date.data
        input_end_date = form.input_end_date.data
        input_interval = form.input_interval.data
        download = form.download.data

        if len(input_ticker) == 0 or len(input_start_date) == 0 or len(input_end_date) == 0 or len(input_interval) == 0:
            error = "Please supply all fields"
        else:
            print(input_ticker)
            print(download)
            d = describe_data(input_ticker, input_start_date, input_end_date, input_interval, download)
            d.get_data()
            return redirect(url_for('register'))

        

    return render_template('register.html', form=form, message=error)

# Run the application
app.run(debug=True)