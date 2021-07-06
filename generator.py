import pandas as pd
import datetime
import math

input_filepath = "./uploads/input.csv"
names_filepath = "./uploads/names.txt"
meta_filepath = "./uploads/meta.txt"

metadata = {
    "start": "",
    "end": "",
    "thres": ""
}

with open(meta_filepath, "r") as meta_file:
    for key, line in zip(metadata, meta_file):
        metadata[key] = line.replace("\n", "")

starting_time = metadata["start"]
ending_time = metadata["end"]
threshold = int(metadata["thres"])

names_list = []
with open(names_filepath, "r") as names_file:
    for line in names_file:
        names_list.append(line)

def maketimestamp(my_string):
    try:
        element = datetime.datetime.strptime(my_string,"%m/%d/%Y, %H:%M:%S")
    except:
        element = datetime.datetime.strptime(my_string,"%m/%d/%Y, %H:%M:%S %p")
  
    timestamp = datetime.datetime.timestamp(element)
    return timestamp

def determineStatus(case, start_time, end_time, threshold, tolerance=0.03333):
    start = float(start_time.split(":")[0]) + float(start_time.split(":")[1])/60
    end = float(end_time.split(":")[0]) + float(end_time.split(":")[1])/60

    threshold /= 60
    finalthres = end-start-threshold-tolerance
    return case > finalthres

def matchname(name, my_list):
    for item in my_list:
        test_case = name.replace(" ", "")
        if test_case == item:
            return test_case
        
        test_case = (name.split(" ")[1] + name.split(" ")[0]).replace(" ", "")
        if test_case == item:
            return test_case
        
        test_case= (name.split(" ")[0] + name.split(" ")[1]).replace(" ", "")
        if test_case == item:
            return test_case

        if len(name.split(" ")) > 2:
            test_case = (name.split(" ")[0] + name.split(" ")[2]).replace(" ", "")
            if test_case == item:
                return test_case

            test_case = (name.split(" ")[2] + name.split(" ")[0]).replace(" ", "")
            if test_case == item:
                return test_case
            
            test_case = (name.split(" ")[1] + name.split(" ")[2] + name.split(" ")[0]).replace(" ", "")
            if test_case == item:
                return test_case
    return name.replace(" ", "")

def international_time(my_time):
    my_time = my_time.strip()
    setting = my_time[len(my_time)-2:]
    date_info = my_time.split(" ")[0]
    time_info = my_time.split(" ")[1]
    hour = int(time_info.split(":")[0])
    remaining_time = ":"+ time_info.split(":")[1]+ ":" + time_info.split(":")[2]
    if setting == "AM" or setting == "PM":
        if setting == "PM":
            if not hour == 12:
                hour += 12
    my_time = date_info + " " + str(hour) + remaining_time

    return my_time

attendence_df = pd.read_csv(input_filepath)
for i in range(len(attendence_df["Full Name"])):
    attendence_df["Full Name"][i] = attendence_df["Full Name"][i].upper()

drop_string = "RITA SHARMA"
drop_indexes = [k for k in attendence_df.loc[attendence_df["Full Name"] == drop_string].index]
attendence_df = attendence_df.drop(drop_indexes, axis=0)

unix = []
new_names = []
for timestamp, name in zip(attendence_df["Timestamp"], attendence_df["Full Name"]):
    unix.append(maketimestamp(international_time(timestamp)))
    new_names.append(name.replace(" ", "").upper())

attendence_df["unix"] = unix
attendence_df["testing names"] = new_names
ending_hour = ending_time.split(":")[0]
ending_minutes = ending_time.split(":")[1]
ending_timestamp = maketimestamp(str(attendence_df["Timestamp"].values[0]).split(",")[0] + f", {ending_hour}:{ending_minutes}:00")

information = {}
for name in names_list:
    information[name] = {
        "time": 0,
        "status": ""
    }

for name in names_list:
    test_name = matchname(name, list(attendence_df["testing names"].values)).replace("\n", "")
    temp = attendence_df.loc[attendence_df["testing names"] == test_name]
    if not len(temp.index) % 2 == 0:
        temp = temp.append({
            "Full Name": name,
            "User Action": "Left",
            "Timestamp": ending_time,
            "unix": ending_timestamp,
            "testing names": test_name
        }, ignore_index=True)
    calculated_time = 0
    length = len(temp["unix"].index)
    i = 0
    while i < length:
        calculated_time += temp["unix"].values[i+1] - temp["unix"].values[i]
        i += 2
    calculated_time /= 3600
    information[name]["time"] = str(calculated_time).split(".")[0] + "hrs " + str(float("0."+str(calculated_time).split(".")[1][:2]) * 60.0).split(".")[0] + "mins"
    information[name]["status"] = "P" if determineStatus(calculated_time, starting_time, ending_time, threshold) else "AB"

final_list = []
for key in information.keys():
    time_temp = information[key]["time"]
    time_string = time_temp.split(".")[0] + str(float())
    final_list.append({
        "Name": key.replace("\n", ""),
        "Time": time_temp,
        "Status": information[key]["status"]
    })

final_df = pd.DataFrame(columns=["Name", "Time", "Status"])
final_df = final_df.append(final_list, ignore_index=True)
output_path = f"./output/generated-attendance.csv"
final_df.to_csv(output_path, index=False)