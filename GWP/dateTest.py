from datetime import datetime, date, timedelta

current = "Jan,27,2021, 9:26 a.m"

datetimeSplit = current.split(" ")

date = datetimeSplit[0].split(",")[:-1]
date_build = date[1]+"-"+date[0]+"-"+date[2]

time_build = datetimeSplit[1].replace(":", ".")+datetimeSplit[2].replace(".","")

datetimeCompile = date_build+" "+time_build

print(datetimeCompile)