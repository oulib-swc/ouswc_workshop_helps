#!/usr/bin/env python
import pandas as pd
import csv


# Read in csv file from EventBrite
# orders = pd.read_csv("report-2016-10-25T2057.csv", index_col='Order #')

orders = ''
file1 = ''
while file1 == '':
    file1 = input('Enter report filename from EventBrite: ')

print(file1)
orders = pd.read_csv(file1, index_col='Order #')

# Read in file list of learners from etherpad (first name last name)
#attendees = pd.read_csv('attendees_2016-10-25-ou.txt', delimiter=' ', header=None, names=['first_name', 'last_name'])

attendees = ''
file2 = ''
while file2 == '':
	file2 = input('Enter list of attendees from etherpad: ')

print(file2)
attendees = pd.read_csv(file2, delimiter=' ', header=None, names=['first_name', 'last_name'])


# In[15]:

attend_list = attendees['last_name'].tolist()
order_list = orders['Last Name'].tolist()

# open files for ouput as csv file

out = open('final_attendenc.csv', 'w')
wr = csv.writer(out, dialect='excel')
wr.writerow(['name', 'email', 'department'])


for index, row in orders.iterrows():
    if row['Last Name'] in attend_list:
        print (row['First Name'], row['Last Name'], '/', row['Email'], '/', row['Department or Center'] )
        wr.writerow([row['First Name'] + ' ' +row['Last Name'],  row['Email'],  row['Department or Center'] ])
    else:
        print (row['First Name'], row['Last Name'], '/', row['Email'], '/', row['Department or Center'] )
        wr.writerow([row['First Name'] + ' ' +row['Last Name']])


out.close()
