import csv, datetime

users = []

with open('data.csv', 'rU') as csvfile:
  reader = csv.DictReader(csvfile)
  users = [ dict([(key,val.strip()) for key,val in row.iteritems()]) for row in reader]
  print users[0].keys()

call_time = "9:00 PM"

for user in users:
  if not user['Birthdate'] or not user['Birthdate'][0:2] != "00": continue
  birthdate = datetime.datetime.strptime(user['Birthdate'], "%m%d%Y")
  print birthdate
  # if birthdate > datetime.datetime.now() - 
