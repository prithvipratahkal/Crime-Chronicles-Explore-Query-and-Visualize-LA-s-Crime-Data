import json

# Function to convert JSON object to a natural language sentence
def json_to_sentence(obj):
    # Extract fields
    date = obj.get("date_occ", "unknown date").split("T")[0]
    time = obj.get("time_occ", "unknown time")
    area = obj.get("area_name", "an unknown area")
    crime = obj.get("crm_cd_desc", "unknown crime")
    location = obj.get("location", "an unknown location")
    premise = obj.get("premis_desc", "unknown premises")
    victim_age = obj.get("vict_age", "unknown age")
    victim_sex = obj.get("vict_sex", "unknown gender")

    if victim_sex == 'M':
        victim_sex = 'Male'
    elif victim_sex == 'F':
        victim_sex = 'Female'
    else:
        victim_sex = 'Gender neutral / Not known' 

    if victim_age == '0' or 0:
        victim_age = 'unknown'

    # Format time as hh:mm
    if isinstance(time, int) and 0 <= time < 2400:
        time_formatted = f"{time // 100:02}:{time % 100:02}"
    else:
        time_formatted = "unknown time"

    # Build the sentence
    sentence = (f"On {date} at {time_formatted}, a crime of type '{crime}' was reported in {area} "
                f"at {location}, near / in {premise}. The victim identifies as {victim_sex}, aged about {victim_age}.")
    return sentence

# Path to the JSON file
input_file = "filtered_la_crime_data.json"  # Replace with your file name
output_file = "data.json"  # The same file to overwrite

# Read the file, process each line, and write back
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        # Parse the JSON object
        json_obj = json.loads(line.strip())

        # Generate the sentence
        sentence = json_to_sentence(json_obj)

        # Update the object with the sentence key
        json_obj["sentence"] = sentence

        # Write the modified object back to the file
        outfile.write(json.dumps(json_obj) + "\n")
