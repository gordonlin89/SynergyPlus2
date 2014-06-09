from pymongo import *
import predictor
import viewer
import random

client = MongoClient('localhost', 27017)
db = client.synergyplus

def schedule_exists(name):
	return db.schedules.find_one({"name": name}) != None

def new_schedule(name):
	if schedule_exists(name):
		raise Exception()
	new_schedule = {"name": name, "event_plans": []}
	schedules = db.schedules
	schedules.insert(new_schedule)

def delete_schedule(name):
	if not schedule_exists(name):
		raise Exception()
	schedules = db.schedules
	schedules.remove({"name": {"$eq": name}})

def get_schedule(name):
	return db.schedules.find_one({"name": name}, {'_id': False})

def get_schedules():
	schedules = db.schedules.find({}, {'_id': False})
	return [schedule for schedule in schedules]

def event_plan_exists(schedule_name, event_plan_name):
	if not schedule_exists(schedule_name):
		raise Exception()
	schedule = db.schedules.find_one({"name": schedule_name}, {'_id': False})
	for event_plan in schedule['event_plans']:
		if event_plan['event_plan'] == event_plan_name:
			return True
	return False

def add_event_plan(schedule_name, event_plan_name, min_temp_business_hours, max_temp_business_hours, min_temp_off_hours, max_temp_off_hours):
	if not schedule_exists(schedule_name):
		raise Exception()
	schedule = db.schedules.find_one({"name": schedule_name}, {'_id': False})
	schedule['event_plans'].append({"event_plan": event_plan_name, "min_temp_business_hours": min_temp_business_hours, "max_temp_business_hours": max_temp_business_hours, "min_temp_off_hours": min_temp_off_hours, "max_temp_off_hours": max_temp_off_hours})
	db.schedules.update({"name": schedule_name}, schedule)

def edit_event_plan(schedule_name, event_plan_name, min_temp_business_hours, max_temp_business_hours, min_temp_off_hours, max_temp_off_hours):
	if not schedule_exists(schedule_name):
		raise Exception()
	schedule = db.schedules.find_one({"name": schedule_name}, {'_id': False})
	for ep in schedule['event_plans']:
		if ep['event_plan'] == event_plan_name:
			ep['min_temp_business_hours'] = min_temp_business_hours
			ep['max_temp_business_hours'] = max_temp_business_hours
			ep['min_temp_off_hours'] = min_temp_off_hours
			ep['max_temp_off_hours'] = max_temp_off_hours
	db.schedules.update({"name": schedule_name}, schedule)

def delete_event_plan(schedule_name, event_plan_name):
	schedule = db.schedules.find_one({"name": schedule_name}, {'_id': False})
	schedule['event_plans'] = [event_plan for event_plan in schedule['event_plans'] if event_plan['event_plan'] != event_plan_name]
	db.schedules.update({"name": schedule_name}, schedule)

def remaining_event_plans(schedule):
	event_plans = ['Weekday', 'Weekend', 'Holiday']
	used = [event_plan['event_plan'] for event_plan in schedule['event_plans']]
	return [event_plan for event_plan in event_plans if event_plan not in used]

def calendar_exists(name):
	return db.calendars.find_one({"name": name}) != None

def new_calendar(name):
	if calendar_exists(name):
		raise Exception()
	new_calendar = {"name": name}
	calendars = db.calendars
	calendars.insert(new_calendar)

def delete_calendar(name):
	if not calendar_exists(name):
		raise Exception()
	calendars = db.calendars
	calendars.remove({"name": {"$eq": name}})

def get_calendars():
	calendars = db.calendars.find({}, {'_id': False})
	return [calendar for calendar in calendars]

def get_prediction(calendar, schedule):
	schedule = get_schedule(schedule)
	try:
		weekday = [ep for ep in schedule['event_plans'] if ep['event_plan'] == 'Weekday'][0]
		min_temp = weekday['min_temp_business_hours']
		temp = min_temp if min_temp !="" else "20"
	except:
		temp = "20"
	return predictor.predict(temp)

def get_history(year):
	return viewer.get_data(year)

def get_avail_history_years():
	return viewer.years

def random_month_data():
	return [random.randint(0, 13) for i in range(12)]
