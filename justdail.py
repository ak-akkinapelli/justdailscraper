from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import csv

def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

def get_location(body):
	text = body.find('a', {'class':'rsmap'})
	if text == None:
		return
	text_list = text['onclick'].split(",")
	
	latitutde = text_list[3].strip().replace("'", "")
	longitude = text_list[4].strip().replace("'", "")
	
	return latitutde + ", " + longitude

page_number = 1
service_count = 1

fields = ['Name', 'Address', 'Location']
out_file = open('tailors.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)


while True:
	# Check if reached end of result
	if page_number > 20:
		break

	url="https://www.justdial.com/Hyderabad/Tailors/nct-10470248"
	print(url)
	req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
	page = urllib.request.urlopen( req )

	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})

	# Iterate through the 10 results in the page
	for service_html in services:

		# Parse HTML to fetch data     
		dict_service = {}
		name = get_name(service_html)
		print(name);
		address = get_address(service_html)
		location = get_location(service_html)
		if name != None:
			dict_service['Name'] = name
		if address != None:
			dict_service['Address'] = address
		if location != None:
			dict_service['Address'] = location

		# Write row to CSV
		csvwriter.writerow(dict_service)

		print("#" + str(service_count) + " " , dict_service)
		service_count += 1

	page_number += 1

out_file.close()
