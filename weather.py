import shutil

import requests
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import re
from googletrans import Translator

# Data extracted from AEMET
# API AEMET OpenData

# TODO: Abstract aemet request to function

def get_weather():
	# Get Aemet information for specific town
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28150',
		params=params)
	# print(aemet_request.json())

	# Get data information
	aemet_data = requests.get(aemet_request.json()['datos']).json()[0]

	# Set information to variables
	date = aemet_data['prediccion']['dia'][0]['fecha']
	dawn = aemet_data['prediccion']['dia'][0]['orto']
	sunset = aemet_data['prediccion']['dia'][0]['ocaso']

	sky_status = aemet_data['prediccion']['dia'][0]['estadoCielo']
	sky_status_next = aemet_data['prediccion']['dia'][1]['estadoCielo']

	temperatures = aemet_data['prediccion']['dia'][0]['temperatura']
	temperatures_next = aemet_data['prediccion']['dia'][1]['temperatura']

	thermal_sensation = aemet_data['prediccion']['dia'][0]['sensTermica']
	thermal_sensation_next = aemet_data['prediccion']['dia'][1]['sensTermica']

	relative_humidity = aemet_data['prediccion']['dia'][0]['humedadRelativa']
	relative_humidity_next = aemet_data['prediccion']['dia'][1]['humedadRelativa']

	# TODO: Two lines per data
	wind = aemet_data['prediccion']['dia'][0]['vientoAndRachaMax']
	wind_next = aemet_data['prediccion']['dia'][1]['vientoAndRachaMax']

	precipitation = aemet_data['prediccion']['dia'][0]['precipitacion']
	precipitation_next = aemet_data['prediccion']['dia'][1]['precipitacion']

	storm_probability = aemet_data['prediccion']['dia'][0]['probTormenta']
	storm_probability_next = aemet_data['prediccion']['dia'][1]['probTormenta']

	snow = aemet_data['prediccion']['dia'][0]['nieve']
	snow_next = aemet_data['prediccion']['dia'][1]['nieve']

	snow_probability = aemet_data['prediccion']['dia'][0]['probNieve']
	snow_probability_next = aemet_data['prediccion']['dia'][1]['probNieve']

	#TODO: Return weather dict
	return temperatures


def get_uv_radiation():
	uv_radiation = []
	for day in range(4):
		aemet_request = requests.get(
			'https://opendata.aemet.es/opendata/api/prediccion/especifica/uvi/' + str(day),
			params=params
		)
		aemet_data = requests.get(aemet_request.json()['datos'])
		aemet_uv_radiation = aemet_data.text.replace('"', '').splitlines()[5:-1]
		uv = [x.rsplit(',', 1) for x in aemet_uv_radiation]
		items = {}
		for key, value in uv:
			items[key] = value

		uv_radiation.append(items)

	return uv_radiation


def satellite_information():

	# Vegetation
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/satelites/producto/nvdi',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/vegetation_index', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/vegetation_index')
	plt.imshow(img)
	plt.show()

	# Sea temperatures
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/satelites/producto/sst',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/sea_temperatures', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/sea_temperatures')
	plt.imshow(img)
	plt.show()

	# Pressure map
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/mapasygraficos/analisis',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/pressure_map', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/pressure_map')
	plt.imshow(img)
	plt.show()

	# Thunders
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/red/rayos/mapa',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/thunders', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/thunders')
	plt.imshow(img)
	plt.show()

	# Fire risks
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/incendios/mapasriesgo/estimado/area/p',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/fire_risk', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/fire_risk')
	plt.imshow(img)
	plt.show()

	# reflectivity
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/red/radar/nacional',
		params=params
	)
	aemet_data = requests.get(aemet_request.json()['datos'], stream=True)
	with open('data/img/reflectivity', 'wb') as f:
		shutil.copyfileobj(aemet_data.raw, f)

	img = mpimg.imread('data/img/reflectivity')
	plt.imshow(img)
	plt.show()


def get_municipalities():
	aemet_request = requests.get(
		'https://opendata.aemet.es/opendata/api/maestro/municipios',
		params=params
	)

	return aemet_request.json()


def get_weather_prediction(date_pred, community_pred=None):
	# TODO: Include table communities

	if community_pred:
		if date_pred == 0:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/' + str(community),
				params=params
			)
		elif date_pred == 1:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/ccaa/manana/' + str(community),
				params=params
			)
		elif date_pred == 2:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/ccaa/pasadomanana/' + str(community),
				params=params
			)
	else:
		if date_pred == 0:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/nacional/hoy/',
				params=params
			)
		elif date_pred == 1:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/nacional/manana/',
				params=params
			)
		elif date_pred == 2:
			aemet_request = requests.get(
				'https://opendata.aemet.es/opendata/api/prediccion/nacional/pasadomanana/',
				params=params
			)

	aemet_data = requests.get(aemet_request.json()['datos'])

	# Split data into lines, removing empty strings
	data = aemet_data.text.splitlines()
	data = [x for x in data if x]
	index = []
	for i in range(len(data)):
		if re.search('.-', data[i]):
			index.append(i)

	# Extract specific data from text
	meteo_phenomenon = ' '.join(data[index[0] + 1:index[1]])
	prediction = ' '.join(data[index[1] + 1:len(data)])
	# print(meteo_phenomenon)
	# print(prediction)

	# Translate data to english
	# TODO: Specify library requirement
	# https://www.thepythoncode.com/article/translate-text-in-python
	translator = Translator()
	meteo_phenomenon = translator.translate(meteo_phenomenon, dest='en').text
	prediction = translator.translate(prediction, dest='en').text

	return meteo_phenomenon, prediction

# Request your personal API key in AEMET and set as environment variable
params = {'api_key': os.environ['API_KEY']}

weather_aemet = get_weather()

# UV Radiation
uv_radiation = get_uv_radiation()
print(uv_radiation)

# Satellite information (vegetation and temperature)
satellite_information()

# Returns all the municipalities of Spain.
municipalities_information = get_municipalities()
# print(municipalities_information)

# General weather predictions.
# Set community to False to get National prediction. Otherwise, set to any community code
# Date codes: (0) today, (1) tomorrow, (2) after tomorrow
# TODO: Test predictions. Based on request data, today is for yesterday
community = 'mad'
date = 0
meteo_phenomenon, weather_prediction = get_weather_prediction(date, community)
print('Significant phenomena: {}'.format(meteo_phenomenon))
print('Weather prediction: {}'.format(weather_prediction))
