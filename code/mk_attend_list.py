#!/usr/bin/env python
import pandas as pd
import csv
import argparse
import sys

parser = argparse.ArgumentParser(
    description='''This script compairs the EventBrite registration with
                   the etherpad sign-ins and outputs a final attendance
                   list with emails and domains if available.


                   The sign-in portion of the etherpad just needs to be of the
                   sign-ins, no header. Keep in mind to check for a Jane Smith
                   who is just a place holder as an example sign-in.''',
    epilog="""Thank you for playing.""")

parser.add_argument('file1', help='The EventBrite report file goes here.')
parser.add_argument('file2', help='The Etherpad sign-in file goes here')
args = parser.parse_args()

if not vars(args):
    parser.print_help()
    parser.exit(1)

# Read in csv file from EventBrite
orders = ''
try:
    orders = pd.read_csv(args.file1, index_col='Order #')
except:
    print('There is a problem with', args.file1)
    sys.exit()

# Read in file list of learners from etherpad (first name last name)
attendees = ''
try:
    attendees = pd.read_csv(args.file2, delimiter=',', header=None,
                            names=['name', 'dept'] + list(range(0, 5)))
#                            names=['first_name', 'last_name'] + list(range(0, 5)))
    # list(range) is needed to account for the copied sign-in list not have the
    # same number of columns for each sign-in. This also is assuming the name fields
    # to only be two parts, first and last and they are the first two items of
    # a sign-in entry.
except:
    print('There is a problem with', args.file2)
    sys.exit()

# Form lists for comparison
# This will be problematic if two learners have the same last name. At that point
# I will need to find another search method for comaring the two lists. It also
# does not take into account typos in the entries by the registrant.
# And make both lists lower case

print(attendees)

attendees_list =  attendees['name'].tolist()
first_list = []
last_list = []

depts =  attendees['dept'].tolist()

for names in attendees_list:
    names = names.strip()
    first, last = names.rsplit(' ',1)
    first_list.append(first)
    last_list.append(last)

# attend_list = attendees['last_name'].tolist()
attend_list = [item.lower() for item in last_list]

order_list = orders['Last Name'].tolist()
order_list = [item.lower() for item in order_list]


# open files for ouput as csv file
out = open('final_attendenc.csv', 'w')
wr = csv.writer(out, dialect='excel')
wr.writerow(['name', 'email', 'department'])

# Check pre-registered in the sign-in list
for index, row in orders.iterrows():
    if row['Last Name'].lower() in attend_list:
        print(row['First Name'], row['Last Name'], '/',
              row['Email'], '/', row['Department or Center'])
        wr.writerow([row['First Name'] + ' ' + row['Last Name'],
                     row['Email'],  row['Department or Center']])

# Now check sign-in learner who may not have pre-register. Walk-ins.
print('----------\n')

count = 0
for item in last_list:
    if item.lower() not in order_list:
        print(count, item,
              'no email or department available')
        wr.writerow([first_list[count] + ' ' + item, depts[count]])
    count += 1

# Close output file.
out.close()
