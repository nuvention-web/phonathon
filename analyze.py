import csv, datetime, sys

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

def find_call_time(user):
	# preprocessing
	if not user['Birthdate'] or not user['Birthdate'][0:2] != "00":
		age = -1
	else:
		age = (datetime.datetime.now() - datetime.datetime.strptime(user['Birthdate'], "%m%d%Y"))
		import pdb; pdb.set_trace()

	# find call time
	pass

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
	for user in users:
		call_time = find_call_time(user)
		user['Call Time'] = call_time
		augmented_users.append(user)

  	with open(csvname,'rU') as csvfile:
  		writer = csv.DictWriter(csvfile,users.keys())
  		for user in augmented_users:
  			writer.writerow(user)
  			if DEBUG: print user