import json

languages = [
	"de",
	"en",
	"es",
	"fr",
	"it",
	"nl"
]

for language in languages:
	
	hours = 0
	minutes = 0
	seconds = 0
	count = 1

	string = ""

	with open("RAL_classic.json", "r") as read_file:
		RAL_colours = json.load(read_file)
	
		for RAL_colour in RAL_colours:
			string += str(count)
			string += "\n"
			string += (f"{hours:02d}:{minutes:02d}:{seconds:02d},000 --> ")
		
			seconds += 1

			if seconds >= 60:
				seconds = 0
				minutes += 1

			if minutes >= 60:
				minutes = 0
				hours += 1

			string += (f"{hours:02d}:{minutes:02d}:{seconds:02d},000")

			string += "\n"

			string += RAL_colour["code"] + " " + RAL_colour["name"][language]
			string += "\n\n"

			count += 1
		
		file_out = open(language + ".srt", "w")
		file_out.write(string)
		file_out.close()

#"de": "Beige",
#"en": "Beige",
#"es": "Beige",
#"fr": "Beige",
#"it": "Beige",
#"nl": "Beige"