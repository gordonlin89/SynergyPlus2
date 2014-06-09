import random
import calendar

years = ['2013', '2014']

total_power = {}
for year in years:
	total_power[year] = [random.randint(0, 13) for i in range(12)]

time = [calendar.month_name[i][0:3] for i in range(1, 13)]

def get_data(year):
	return [i for i in zip(time, total_power[year])]
