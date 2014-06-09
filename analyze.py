import os, csv, datetime, sys, pickle

from utils import get_tz_for_city

# users = []

# with open('data.csv', 'rU') as csvfile:
#   reader = csv.DictReader(csvfile)
#   users = [ dict([(key,val.strip()) for key,val in row.iteritems()]) for row in reader]
#   print users[0].keys()

# call_time = "9:00 PM"

# for user in users:
#   if not user['Birthdate'] or not user['Birthdate'][0:2] != "00": continue
#   birthdate = datetime.datetime.strptime(user['Birthdate'], "%m%d%Y")
#   print birthdate
  # if birthdate > datetime.datetime.now() - 

EASTERN_TZ = -4.0
CENTRAL_TZ = -5.0
MOUNTAIN_TZ = -6.0
PACIFIC_TZ = -7.0

def find_call_time(user):

	# preprocessing
	if not user['Birthdate'] or not user['Birthdate'][0:2] != "00":
		age = -1
	else:
		age = (datetime.datetime.now().year - datetime.datetime.strptime(user['Birthdate'], "%m%d%Y").year)

	if not user['Child1Name']:
		child = -1
	else:
		child = True

	timezone = get_tz_for_city(user['City'], user['State'])

	###############################################################

	call_times = {
		'Day Time': 0,
		'6:00-6:30': 0,
		'6:30-7:00': 0,
		'7:00-7:30': 0,
		'7:30-8:00': 0,
		'8:00-8:30': 0,
		'8:30-9:00': 0,
		'9:00-9:30': 0
	}

	if age >= 65:
		call_times['Day Time'] += 1
	else:
		if child:
			call_times['6:00-6:30'] += 1.5
			call_times['6:30-7:00'] += 1.5
			call_times['7:00-7:30'] += 1.5
		
		if age >= 43:
			call_times['6:00-6:30'] += 1
			call_times['6:30-7:00'] += 1
			call_times['7:00-7:30'] += 1

		if age < 43:
			call_times['7:30-8:00'] += 1
			call_times['8:00-8:30'] += 1
			call_times['8:30-9:00'] += 1
			call_times['9:00-9:30'] += 1

		if timezone == MOUNTAIN_TZ or timezone == PACIFIC_TZ:
			call_times['6:00-6:30'] += 1.5
			call_times['6:30-7:00'] += 1.5
			call_times['7:00-7:30'] += 1.5
			call_times['7:30-8:00'] += 1.5
		elif timezone == EASTERN_TZ:
			call_times['8:30-9:00'] = 0
			call_times['9:00-9:30'] = 0
			call_times['6:30-7:00'] -= 1.5
			call_times['7:00-7:30'] -= 1.5
		elif timezone == CENTRAL_TZ:
			call_times['7:30-8:00'] -= 1.5
			call_times['8:00-8:30'] -= 1.5
		else:
			pass # where da fuq r u mayne
	
	return call_times

DEBUG = True

if __name__ == "__main__":

	if len(sys.argv) > 1:
		csvname = sys.argv[1]
	else:
		csvname = 'data.csv'

	with open(csvname, 'rU') as csvfile:
  		reader = csv.DictReader(csvfile)
  		users = [ dict([(key,val.strip()) for key,val in row.iteritems()]) for row in reader]
  		if DEBUG: print users[0].keys()

	augmented_users = []
	cities_states = set()

	if os.path.isfile('timezones.pickle'):
		cities_states_dict = pickle.load(open('timezones.pickle', "rb" ))
	else:
		cities_states_dict = {}

	if os.path.isfile('states_timezones.pickle'):
		states_dict = pickle.load(open('states_timezones.pickle', "rb" ))
	else:
		states_dict = {}

	for user in users:
		# call_time = find_call_time(user)
		# print call_time
		city_state = "%s %s" % (user['City'], user['State'])
		cities_states.add(city_state)

		print city_state

		if user['State'] not in ['ID', 'OR', 'KS', 'NE', 'SD', 'ND', 'TX', 'FL', 'IN', 'MI', 'KY', 'TN', 'AK']:
			if user['State'] not in states_dict:
				states_dict[user['State']] = get_tz_for_city(user['City'], user['State'])
				pickle.dump(states_dict, open('states_timezones.pickle', 'w'))
		else:

			if city_state not in cities_states_dict:
				cities_states_dict[city_state] = get_tz_for_city(user['City'], user['State'])
				pickle.dump(cities_states_dict, open('timezones.pickle', 'w'))

		# user['Call Time'] = call_time
		augmented_users.append(user)

	

	print len(cities_states)
	print cities_states

  	with open(csvname,'rU') as csvfile:
  		writer = csv.DictWriter(csvfile,users.keys())
  		for user in augmented_users:
  			writer.writerow(user)
  			if DEBUG: print user