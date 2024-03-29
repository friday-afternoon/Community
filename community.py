#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  community.py
#  
#  Copyright 2017-2019 Hisen Zhang <hisenzhang@Zhang>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import division
import sys
import requests 
import re	
import json
from prettytable import PrettyTable as pt

# The main process of community.py
def com(): 

	# Create two files to used. 
	# data.json is for JSON format
	# datatable.txt is for mankind reading 

	f = open('data.json','w+')
	t = open('datatable.txt','w+')

	# Create and initialize the datatable

	x = pt(["NO.","Code","Name","Area","Green Coverage"]) 

	# Check Info

	print '\033[2J\033[HData on monitoring. Requesting data from Internet...'

	# Page loop
	# 318 as upper boundry, 10~ for DEMO

	for j in range(1,10):	

		# Progression bar

		print '\nSector',j,'of 317\n'
		
		# Get URL

		r = requests.get(url = 'http://hangzhou.fangtoo.com/building/cp' + str(j))
		
		# Get the name list from page loop

		name = re.findall(r'<a href=["]http://hangzhou.fangtoo.com/building/(.*)/["] target=["]_blank["] title=["](.*)["] target=["]_blank["]>',r.text)
		
		# Leave blank 1

		x.padding_width = 1

		# Item loop

		for i in range(1,len(name)):
			
			# Get info from URL

			detail = requests.get(url = 'http://hangzhou.fangtoo.com/building/' + str(name[i-1][0]))
			
			# Pick info from detail

			area = re.findall(ur'<li>占地面积：(\d.*)平方米</li>',detail.text) 
			ve = re.findall(ur'<li>绿化率：(.*)</li>',detail.text)
			
			# Have '--' if area is missing

			if area == []:
				area = [('--')]
			
			# Set varibles

			CODE = str(i+(j-1)*26)
			ID = str(name[i-1][0].encode('utf-8'))
			NAME = str(name[i-1][1].encode('utf-8'))
			AREA = str(area[0].encode('utf-8'))
			GREEN_COVERAGE = str(ve[0].encode('utf-8'))

			# Generate strings based on these varibles

			json_data = json.dumps({'NO.':CODE.zfill(4),'ID':ID,'NAME':NAME,'AREA':AREA,'GREEN_COVERAGE':GREEN_COVERAGE})
			table_data = ([CODE.zfill(4),ID,NAME,AREA,GREEN_COVERAGE])
			
			# Print strings to screen in a human-friendly manner

			print CODE.zfill(4),ID,NAME,AREA,GREEN_COVERAGE
			
			# Write strings into JSON file on disk

			x.add_row(table_data)
			f.writelines(json_data) 
		
	# Print the table

	print x
	
	# Write table into the file on disk

	t.writelines(str(x)) 

	# Save and close two files

	f.close
	t.close
	
	# Output

	print 'All requests successfully recorded.'

# The part of statistics

def sta():

	# Load data from JSON record

	with open('data.json','r+') as f:
		x = f.readlines()
	
	# check the valid data from records

	l = re.findall(r'["]([0-9]*[\.]*[0-9]+)%["]',str(x))
	print len(l),'data is valid for statistic.\n'
	
	# Initialize the counters

	counter_0 = 0
	counter_1 = 0
	counter_2 = 0
	counter_3 = 0
	counter_4 = 0

	# Classify all available data
	
	for i in range(0,len(l)):
		if float(l[i])<10:
			counter_0 = counter_0 + 1
		if float(l[i])>=10 and float(l[i])<25:
			counter_1 = counter_1 + 1
		if float(l[i])>=25 and float(l[i])<40:
			counter_2 = counter_2 + 1
		if float(l[i])>=40 and float(l[i])<55:
			counter_3 = counter_3 + 1
		if float(l[i])>55:
			counter_4 = counter_4 + 1
			return 0

	# Create table, ranking 

	tb = pt(["RANGE","COUNT","PERCENTAGE",]) 	
	tb.align["COUNT"] = "r" 
	tb.add_row(["x<10",counter_0,float(counter_0/len(l)*100)])
	tb.add_row(["10<=x<25",counter_1,float(counter_1/len(l)*100)])
	tb.add_row(["25<=x<40",counter_2,float(counter_2/len(l)*100)])
	tb.add_row(["40<=x<55",counter_3,float(counter_3/len(l)*100)])	
	tb.add_row(["x>55",counter_4,float(counter_4/len(l)*100)])
	print tb

# Main function

def main(args):
	com()
	sta()
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
