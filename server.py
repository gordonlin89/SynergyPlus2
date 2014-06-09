from bottle import *
import mediator

@route('/css/<filename>')
def js(filename):
	return static_file(filename, root='./css')

@route('/js/<filename>')
def css(filename):
	return static_file(filename, root='./js')

@route('/img/<filename>')
def img(filename):
	return static_file(filename, root='./img')

@route('/building')
def building():
	return jinja2_template('building.html')

@route('/calendar')
def calendar():
	calendars = mediator.get_calendars()
	return jinja2_template('calendar.html', calendars=calendars)

@post('/calendar')
def calendar():
	#Handle creating new schedules
	new_calendar_name = request.forms.get('new_calendar')
	if new_calendar_name and not mediator.calendar_exists(new_calendar_name):
		mediator.new_calendar(new_calendar_name)
	#Delete schedules
	delete_calendar_name = request.forms.get('delete_calendar')
	if delete_calendar_name and mediator.calendar_exists(delete_calendar_name):
		mediator.delete_calendar(delete_calendar_name)
	#Serve HTML
	calendars = mediator.get_calendars()
	return jinja2_template('calendar.html', calendars=calendars)

@route('/calendar/<calendar_name>')
def calendar_edit(calendar_name):
	return jinja2_template('calendar_edit.html', calendar_name=calendar_name)

@route('/building/<building_name>/overview')
def overview(building_name):
	return jinja2_template('building_overview.html')

@route('/building/<building_name>/history')
def history(building_name):
	year = request.query.get('year')
	if year is None:
		data = []
	else:
		data = mediator.get_history(year)
	years = mediator.get_avail_history_years()
	return jinja2_template('building_history.html', years=years, data=data)

@route('/building/<building_name>/schedule')
def schedule(building_name):
	schedules = mediator.get_schedules()
	return jinja2_template('building_schedule.html', schedules=schedules)

@post('/building/<building_name>/schedule')
def schedule(building_name):
	#Handle creating new schedules
	new_schedule_name = request.forms.get('new_schedule')
	if new_schedule_name and not mediator.schedule_exists(new_schedule_name):
		mediator.new_schedule(new_schedule_name)
	#Delete schedules
	delete_schedule_name = request.forms.get('delete_schedule')
	if delete_schedule_name and mediator.schedule_exists(delete_schedule_name):
		mediator.delete_schedule(delete_schedule_name)
	#Serve HTML
	schedules = mediator.get_schedules()
	return jinja2_template('building_schedule.html', schedules=schedules)

@route('/building/<building_name>/schedule/<schedule_name>')
def schedule_edit(building_name, schedule_name):
	schedule = mediator.get_schedule(schedule_name)
	remaining_event_plans = mediator.remaining_event_plans(schedule)
	disabled = "disabled" if not remaining_event_plans else ""
	return jinja2_template('building_schedule_edit.html', schedule=schedule, remaining_event_plans=remaining_event_plans, disabled=disabled)

@post('/building/<building_name>/schedule/<schedule_name>')
def schedule_edit(building_name, schedule_name):
	action = request.forms.get('action')
	event_plan = request.forms.get('event_plan')
	
	if action == 'new':
		mediator.add_event_plan(schedule_name, event_plan, "", "", "", "")
	elif action == 'edit':
		min_temp_business_hours = request.forms.get('min_temp_business_hours')
		max_temp_business_hours = request.forms.get('max_temp_business_hours')
		min_temp_off_hours = request.forms.get('min_temp_off_hours')
		max_temp_off_hours = request.forms.get('max_temp_off_hours')
		mediator.edit_event_plan(schedule_name, event_plan, min_temp_business_hours, max_temp_business_hours, min_temp_off_hours, max_temp_off_hours)
	elif action == 'delete':
		mediator.delete_event_plan(schedule_name, event_plan)
	else:
		raise Exception()
	
	schedule = mediator.get_schedule(schedule_name)
	remaining_event_plans = mediator.remaining_event_plans(schedule)
	disabled = "disabled" if not remaining_event_plans else ""
	return jinja2_template('building_schedule_edit.html', schedule=schedule, remaining_event_plans=remaining_event_plans, disabled=disabled)

@route('/building/<building_name>/predict')
def predict(building_name):
	calendars = mediator.get_calendars()
	schedules = mediator.get_schedules()
	years = mediator.get_avail_history_years()
	return jinja2_template('building_predict.html', years=years, calendars=calendars, schedules=schedules)

@post('/data')
def data():
	calendar = request.forms.get('calendar')
	schedules = request.forms.getall('schedule')
	histories = request.forms.getall('history')
	
	import calendar
	import random
	time = [calendar.month_name[i][0:3] for i in range(1, 13)]
	series = {}
	for schedule in schedules:
		if schedule.startswith('energyplus'):
			series[schedule] = mediator.get_prediction(None, schedule)
		else:
			series[schedule] = mediator.random_month_data()
	for history in histories:
		series[history] = [i for i in zip(*mediator.get_history(history))][-1]
	return {"time":time, "series": series}

run(host='localhost', port=8080)
