from bs4 import BeautifulSoup
import requests, json

base_url = "https://www.ralcolorchart.com"

hue_urls = [
	"https://www.ralcolorchart.com/ral-classic/yellow-hues",
	"https://www.ralcolorchart.com/ral-classic/orange-hues",
	"https://www.ralcolorchart.com/ral-classic/red-hues",
	"https://www.ralcolorchart.com/ral-classic/violet-hues",
	"https://www.ralcolorchart.com/ral-classic/blue-hues",
	"https://www.ralcolorchart.com/ral-classic/green-hues",
	"https://www.ralcolorchart.com/ral-classic/grey-hues",
	"https://www.ralcolorchart.com/ral-classic/brown-hues",
	"https://www.ralcolorchart.com/ral-classic/white-and-black-hues"
]

def rgb_to_hex(r, g, b):
	return '#{:02X}{:02X}{:02X}'.format(r, g, b)

colour_data = []

for hue_url in hue_urls:
	hue_page = requests.get(hue_url)
	soup_hue = BeautifulSoup(hue_page.content, "lxml")

	colours_div = soup_hue.find("div", class_="colors")
#	colour_links = soup_hue.find_all("a", class_="reverse")
	colour_links = colours_div.find_all("a")
	for colour_link in colour_links:
		code = colour_link.text
		colour_url = base_url + colour_link.get("href")

		colour_page = requests.get(colour_url)
		soup_colour = BeautifulSoup(colour_page.content, "lxml")

		# RGB
		row = soup_colour.find("span", title="Red").parent.parent
		red = int(row.find("td").text)
		row = soup_colour.find("span", title="Green").parent.parent
		green = int(row.find("td").text)
		row = soup_colour.find("span", title="Blue").parent.parent
		blue = int(row.find("td").text)

		# CMYK
		row = soup_colour.find("span", title="Cyan").parent.parent
		cyan = int(row.find("td").text)
		row = soup_colour.find("span", title="Magenta").parent.parent
		magenta = int(row.find("td").text)
		row = soup_colour.find("span", title="Yellow").parent.parent
		yellow = int(row.find("td").text)
		row = soup_colour.find("span", title="Key").parent.parent
		key = int(row.find("td").text)

		# Hex code
		hex = rgb_to_hex(red, green, blue)

		# Names
		english = colour_link.get("title")
		english = english.partition(code + " ")[2]
		row = soup_colour.find("th", string="Color name Dutch:").parent
		dutch = row.find("td").text
		row = soup_colour.find("th", string="Color name German:").parent
		german = row.find("td").text
		row = soup_colour.find("th", string="Color name French:").parent
		french = row.find("td").text
		row = soup_colour.find("th", string="Color name Italian:").parent
		italian = row.find("td").text
		row = soup_colour.find("th", string="Color name Spanish:").parent
		spanish = row.find("td").text

		data = {
			"code": code,
			"colour": {
				"rgb": {
					"r": red, "g": green, "b": blue
				},
				"cmyk": {
					"c": cyan, "m": magenta, "y": yellow, "k": key
				},
				"hex": hex
			},
			"name": {
				"de": german,
				"en": english,
				"es": spanish,
				"fr": french,
				"it": italian,
				"nl": dutch
			}
		}

		colour_data.append(data)

with open('/Users/tom/Documents/GitHub/Fusion-360-Scripts/RAL_colour_cycle/RAL_classic.json', 'w', encoding='latin-1') as f:
	#json.dump(colour_data, f, indent=8, ensure_ascii=False)
	json.dump(colour_data, f, indent='\t', separators=(',', ': '))
