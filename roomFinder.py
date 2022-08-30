import requests
import json

class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
caching = True
fetch = True
department = ["ACFN", "AE", "ARE", "ARC", "MBA", "CHE", "CHEM", "CRP", "CE", "COE", "CEM", "CIE", "EE", "ELD", "ELI", "ERTH", "GS", "SE", "ICS", "ISOM", "IAS", "LS", "MGT", "MSE", "MATH", "ME", "CPG", "PETE", "PE", "PHYS", "PSE"]
while True:
    jsons = {"array": []}
    while True:
        term = input(f"{colors.ENDC}Please enter the {colors.BOLD}term{colors.ENDC} number (for example 212): ")
        choice = ""
        import os.path
        from os import path

        # Find if term exists
        if (requests.get(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code=20{term}0&department_code=CHE").content == b'{"data": []}'):
            print(f"{colors.ENDC}{colors.FAIL}This term is unavailable!{colors.ENDC}")
            continue
        else:
            break

    # Find if cached
    if (path.exists(f"{term}.json")):
        while choice == "":
            choice = input(f"{colors.ENDC}A cached version of the sections is found on this machine, {colors.BOLD}use it to save time?{colors.ENDC} (Y/N): ")
            if not ((choice.lower() == "y") or (choice.lower() == "n")):
                print(f"{colors.ENDC}{colors.FAIL}Please choose a valid option..{colors.ENDC}")
                choice = ""
        if choice == "y" or choice == "Y":
            fetch = False
        else:
            fetch = True

    # If not cached, fetch!  
    if fetch:
        with open(f'{term}.json', 'w') as outfile:
            for course in department:
                URL = f"https://registrar.kfupm.edu.sa/api/course-offering?term_code=20{term}0&department_code={course}"
                courses = requests.get(URL).json()
                print(f"{colors.ENDC}Fetching: {colors.OKGREEN}{course}{colors.ENDC}")
                jsons["array"].append(courses)
            json.dump(jsons, outfile)

    flag3 = True
    while flag3:
        day = input(f"{colors.ENDC}Please enter a {colors.BOLD}day{colors.ENDC} (for example U or W): ").upper()
        if day == "U" or day == "M" or day == "T" or day == "W" or day == "R":
            flag3 = False
        else:
            print(f"{colors.ENDC}{colors.FAIL}Please enter a proper day.{colors.ENDC}")

    flag4 = True
    while flag4:
        building = input(f"{colors.ENDC}Please enter a {colors.BOLD}building{colors.ENDC} or {colors.BOLD}leave blank{colors.ENDC} for all buildings (for example 22 or 24): ")
        if building.isnumeric() or building == "":
            flag4 = False
        else:
            print(f"{colors.ENDC}{colors.FAIL}Please enter a proper building.{colors.ENDC}")

    flag1 = True
    while flag1:
        start_time = input(f"{colors.ENDC}Please enter the {colors.BOLD}start time{colors.ENDC} (for example 1400 or 900): ")
        if start_time.isnumeric() and (len(start_time) == 3 or len(start_time) == 4):
            flag1 = False
        else:
            print(f"{colors.ENDC}{colors.FAIL}Please enter a proper start time.{colors.ENDC}")

    flag2 = True
    while flag2:
        end_time = input(f"{colors.ENDC}Please enter the {colors.BOLD}end time{colors.ENDC} (for example 2200 or 1800): ")
        if end_time.isnumeric() and (len(end_time) == 3 or len(end_time) == 4):
            flag2 = False
        else:
            print(f"{colors.ENDC}{colors.FAIL}Please enter a proper end time.{colors.ENDC}")

    removed = []
    included = []
    with open(f"{term}.json", "r") as f:
        json_data = json.loads(f.read())
        for request in json_data["array"]:
            for section in request["data"]:         
                if section["start_time"] == None or section["end_time"] == None or section["building"] == None or section["class_days"] == None or section["room"] == None:
                    continue
                if building == "":
                    if (int(section["end_time"]) - int(start_time) <= 0 or int(end_time) - int(section["start_time"]) <= 0):
                        pass
                    else:
                        if day not in section["class_days"]:
                            pass
                        elif (section["building"], section["room"]) not in removed:
                            removed.append((section["building"], section["room"]))
                        else:
                            continue
                else:
                    if (int(section["end_time"]) - int(start_time) <= 0 or int(end_time) - int(section["start_time"]) <= 0) and building == section["building"]:
                        pass
                    else:
                        if day not in section["class_days"] and building == section["building"]:
                            pass
                        elif (section["building"], section["room"]) not in removed:
                            removed.append((section["building"], section["room"]))
                        else:
                            continue
    remove = False
    with open(f"{term}.json", "r") as f:
        json_data = json.loads(f.read())
        for request in json_data["array"]:
            for section in request["data"]: 
                if section["start_time"] == None or section["end_time"] == None or section["building"] == None or section["class_days"] == None or section["room"] == None:
                    continue
                for sec_building, sec_room in removed:
                    remove = False
                    if sec_building == section["building"] and sec_room == section["room"]:
                        remove = True
                        break
                if not remove:
                    if f'{colors.ENDC}Building: {colors.BOLD}{colors.OKBLUE}{section["building"]}{colors.ENDC}\t | Room: {colors.BOLD}{colors.OKBLUE}{section["room"]}{colors.ENDC}' not in included:
                        included.append(f'{colors.ENDC}Building: {colors.BOLD}{colors.OKBLUE}{section["building"]}{colors.ENDC}\t | Room: {colors.BOLD}{colors.OKBLUE}{section["room"]}{colors.ENDC}')

    included.sort()
    for available_class in included:          
        print(available_class)
    again = ""
    while True:
        again = input(f"{colors.ENDC}Do you want to {colors.BOLD}search again{colors.ENDC}(Y/N)? ")
        if (again.lower() == "n" or again.lower() == "y"):
            if (again.lower() == "n"):
                exit()
            else:
                break
        else:
            print(f"{colors.ENDC}{colors.FAIL}Please enter either Y or N!{colors.ENDC}")
