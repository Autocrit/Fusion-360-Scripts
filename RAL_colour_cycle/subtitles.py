import json

languages = [
	"de",
	"en",
	"es",
	"fr",
	"it",
	"nl"
]

# Duration in seconds
duration_seconds = 3

def convert_milliseconds(milliseconds):
	seconds, milliseconds = divmod(milliseconds, 1000)
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)

	return hours, minutes, seconds, milliseconds

for language in languages:
	count = 1
	string = ""
 	
	with open("RAL_classic.json", "r") as read_file:
		RAL_colours = json.load(read_file)
	
		for RAL_colour in RAL_colours:
			time_milliseconds = (count -1) * duration_seconds * 1000
			hours, minutes, seconds, milliseconds = convert_milliseconds(time_milliseconds)

			string += str(count)
			string += "\n"
			string += (f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d} --> ")
		
			time_milliseconds += duration_seconds * 1000 - 1

			hours, minutes, seconds, milliseconds = convert_milliseconds(time_milliseconds)

			string += (f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}")

			string += "\n"

			string += RAL_colour["code"] + " " + RAL_colour["name"][language]
			string += "\n\n"

			count += 1
		
		file_out = open(language + "_3.srt", "w")
		file_out.write(string)
		file_out.close()
