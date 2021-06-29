#Open command prompt and change directory to the folder where this code is saved
# before running the file run the following 2 commands to install streamlit and yfinance. Install other dependecies if required using pip command
# pip install streamlit 
# pip install yfinance 
# run the file using the command in the command prompt in the directory of the code: streamlit run get_data.py  


import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
import subprocess
import speech_recognition as sr

# from matplotlib.widgets import Cursor
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# plt.style.use('seaborn')


class describe_data:

	def __init__(self, ticker, start_date, end_date, interval, download_data):
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = end_date
		self.interval = interval 
		self.download_data = download_data

	def get_data(self):
		self.sd = datetime(int(self.start_date.split("-")[0]), int(self.start_date.split("-")[1]), int(self.start_date.split("-")[2]))
		self.ed = datetime(int(self.end_date.split("-")[0]), int(self.end_date.split("-")[1]), int(self.end_date.split("-")[2]))
		self.df = yf.download(tickers = self.ticker, start = self.sd, end = self.ed, interval = self.interval)
		self.df = self.df.reset_index()
		self.df['Date'] = self.df['Datetime'].map(lambda x: pd.to_datetime(x).date())
		self.df['Time'] = self.df['Datetime'].map(lambda x: pd.to_datetime(x).time())
		self.df = self.df.drop(['Datetime'], axis = 1)
		self.df['date_time'] = self.df['Date'].map(lambda x:str(x.month)) + '-' + self.df['Date'].map(lambda x:str(x.day)) + ' ' + self.df['Time'].map(lambda x:str(x.hour)) + ":" +  self.df['Time'].map(lambda x:str(x.minute))
		self.col_order = ['Date','Time','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'date_time']

		if self.download_data:
			file_name = self.ticker + '_' + str(self.sd.month) + '-' + str(self.sd.day) + '_to_' + str(self.ed.month) + '-' + str(self.ed.day) + '.xlsx'
			self.df[self.col_order].to_excel(file_name)
			print('download ho rela hai: ', file_name)
		else:
			pass
		# print(self.df)
		return self.df

	def plot_data(self):
		self.temp_data = self.get_data()
		fig = plt.figure()
		ax = fig.subplots()
		ax.plot(self.temp_data['date_time'],self.temp_data['Adj Close'], color = 'r')
		# ax.set_title(self.ticker + " Adj Close Price Between " + str(datetime(self.start_date,self.end_date).strftime("%B")), fontweight="bold", size=20, color = 'white')
		
		plt.xticks(rotation = 90)
		# cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,color = 'r', linewidth = 1)
		# annot = ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points", bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),arrowprops=dict(arrowstyle='-|>'))
		# annot.set_visible(False)
		# def onmotion(event):
		# 	x = event.xdata
		# 	y = event.ydata
		# 	annot.xy = (x,y)
		# 	text = "{:.4f}".format(event.ydata)
		# 	annot.set_text(text)
		# 	annot.set_visible(True)
		# 	fig.canvas.draw()
		
		# fig.canvas.mpl_connect('motion_notify_event', onmotion)

		# st.plotly_chart(fig, figwidth=1100,height=900)

		plt.show()

default_start = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day-2)
default_end = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day-1)

class DataRequestForm(FlaskForm):
	input_ticker = TextField('Ticker', default = 'TATAMOTORS.NS')
	input_start_date = TextField('Start Date', default = default_start)
	input_end_date = TextField('End Date', default=default_end)
	input_interval = TextField('Interval', default='5m')
	download = BooleanField('Download Data')
	generate_chart = BooleanField('Generate Chart')


def bytes_to_wavfile(bytes_obj):
	# add filepath variables as config later, to make this more general
	# right now this function returns the filename
	# to be used for the 'convert_webm_to_wav' function
	# NOTE: separate this functionality
	file_ext = '.webm'
	_name = (str(datetime.now()).replace('-', '_').replace(' ', '_').replace(':', '_')).split('.')[0]
	file_path = os.path.join('web_app', 'static', _name) 
	file_name = file_path + file_ext
	with open(file_name, mode='bx') as f:
		f.write(bytes_obj)
	f.close()
	print('saved .webm file at: ', file_name)
	return file_path


def convert_webm_to_wav(infile, outfile):
	command = ['ffmpeg', '-i', infile, '-vn', outfile]
	subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	print('------------- conversion complete-------------------')


def clean_directory(infile, outfile):
	os.remove(infile)
	os.remove(outfile)
	print('cleaned clean_directory. deleted files: ', infile, ' & ', outfile)
# default_start = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day-1)
# default_end = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)


def recognize_speech(AUDIO_FILE):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)
        print('* * * * *')
        print('\n')
        print("Google Speech Recognition prediction >> " + speech)
        print('\n')
        print('* * * * *')
        return speech
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "Could not request results from Google Speech Recognition service; {0}".format(e)    


# st.write("Enter yfinance Company Ticker")

# input_ticker = st.text_input("Ticker", value = 'TATAMOTORS.NS')

# st.write('Enter start date in format yyyy-mm-dd')

# input_start_date = st.text_input('Start Date', value = default_start )

# st.write('Enter end date in format yyyy-mm-dd')

# input_end_date = st.text_input("End Date", value = default_end)

# st.write('Enter interval for data (valid 5m etc, unit is minute)')
# input_interval = st.text_input("Interval", value = '5m')

# download_button = st.button("Download")

# d = describe_data(input_ticker,input_start_date, input_end_date, input_interval, download_button)
# d.plot_data()




# def get_yfinance_data(ticker, start_date, end_date):
# 	sd = datetime(*[int(x) for x in start_date.split("-")])
# 	ed = datetime(*[int(x) for x in end_date.split("-")])
# 	df = yf.download(tickers=ticker, start=sd, end=ed, interval=interval)

# 	return df

# def set_data(yf_df):
# 	df = yf_df.reset_index()
# 	df['Date'] = df['Datetime'].map(lambda x: pd.to_datetime(x).date())
# 	df['Time'] = df['Datetime'].map(lambda x: pd.to_datetime(x).time())
# 	df = df.drop(['Datetime'], axis = 1)
# 	df['date_time'] = df['Date'].map(lambda x:str(x.month)) + '-' + df['Date'].map(lambda x:str(x.day)) + ' ' + df['Time'].map(lambda x:str(x.hour)) + ":" +  df['Time'].map(lambda x:str(x.minute))
# 	col_order = ['Date','Time','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'date_time']
# 	return df[col_order]

# def download_data(df, ticker, ed):
# 	file_name = ticker + ' ' + str(ed.month) + '-' + str(ed.day) + '.xlsx'
# 	df.to_excel(file_name)
# 	print('Saved file to disk as: ', file_name)
# 	# if file_ext == 'xlsx':
# 	# 	file_name = ticker + ' ' + str(ed.month) + '-' + str(ed.day) + '.xlsx'
# 	# else if file_ext == 'csv':
# 	# 	file_name = ticker + ' ' + str(ed.month) + '-' + str(ed.day) + '.csv'


