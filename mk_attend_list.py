#!/usr/bin/env python
import pandas as pd
import csv
import argparse
import sys

parser=argparse.ArgumentParser(
    description='''This script compairs the EventBrite registration with
                    the etherpad sign-ins and outputs a final attendance
                    list with emails and domains if available.

                
                    The list of learners needs to be edited to only include
                    the first and last names of the attendees''',
    epilog="""Thank you for playing.""")
args=parser.parse_args()


# Read in csv file from EventBrite
orders = ''
file1 = ''
try:
    while file1 == '':
        file1 = input('Enter report filename from EventBrite: ')
    orders = pd.read_csv(file1, index_col='Order #')
except:
    print (file1, "does not exist")
    sys.exit()

# Read in file list of learners from etherpad (first name last name)
attendees = ''
# file2 = './2017-03-13-sign-in_list.txt'
file2 = ''
try:
    while file2 == '':
    	file2 = input('Enter list of attendees from etherpad: ')

    attendees = pd.read_csv(file2, delimiter=' ', header=None, names=['first_name', 'last_name'])
except:
    print(file2, 'does not exist')
    sys.exit()

# Form lists for comparison
attend_list = attendees['last_name'].tolist()
order_list = orders['Last Name'].tolist()

# make lists lower case
attend_list = [item.lower() for item in attend_list]
order_list = [item.lower() for item in order_list]


# open files for ouput as csv file
out = open('final_attendenc.csv', 'w')
wr = csv.writer(out, dialect='excel')
wr.writerow(['name', 'email', 'department'])

# test for EventBrite sign-up with attendee sign-in
# for index, row in orders.iterrows():
#     if row['Last Name'].lower() in attend_list:
#         print (row['First Name'], row['Last Name'], '/', row['Email'], '/', row['Department or Center'] )
#         wr.writerow([row['First Name'] + ' ' +row['Last Name'],  row['Email'],  row['Department or Center'] ])
#     else:
#         print (row['First Name'], row['Last Name'], 'no email or department available' )
#         wr.writerow([row['First Name'] + ' ' +row['Last Name']])

# Check for learns who pre-registered
for index, row in orders.iterrows():
    if row['Last Name'].lower() in attend_list:
        print (row['First Name'], row['Last Name'], '/', row['Email'], '/', row['Department or Center'] )
        wr.writerow([row['First Name'] + ' ' +row['Last Name'],  row['Email'],  row['Department or Center'] ])
# Now check for learner who attended and did not pre-register
for index,row in attendees.iterrows():
    if row['last_name'].lower() not in order_list:
        print (row['first_name'], row['last_name'], 'no email or department available' )
        wr.writerow([row['first_name'] + ' ' +row['last_name']])


out.close()
