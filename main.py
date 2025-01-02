# Copyright (c) 2025 Omer Drkić
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at https://www.boost.org/LICENSE_1_0.txt)

import colorama
import ctypes
import os
import random
import re
import shutil
import stat
import sys
import time
import win32api

colorama.init()

email = colorama.Fore.LIGHTBLUE_EX + "omerdrkic2501@gmail.com" + colorama.Fore.RESET

def abort(code: int, string: str = ""):
    if string:
        sys.stderr.write(colorama.Fore.LIGHTRED_EX + string + colorama.Fore.RESET)
        sys.stderr.flush()
    exit(code)

def prompt(msg: str):
    confirm = input(f"{msg} (Y/n) {colorama.Fore.LIGHTBLACK_EX}").lower()
    print(colorama.Fore.RESET, end = "")
    while confirm not in "yn":
        confirm = input(
            f"Please enter a valid option. (Y/n) {colorama.Fore.LIGHTBLACK_EX}"
        ).lower()
        print(colorama.Fore.RESET, end = "")
    return confirm == "y"

os.system("@echo off")

if not ctypes.windll.shell32.IsUserAnAdmin():
    abort(2, "The script needs admin privileges to operate.")
elif len(sys.argv) < 2:
    abort(2, "Expected a drive name.")
elif len(sys.argv) > 2:
    abort(2, "Too many arguments.")

drive = sys.argv[1]

if not re.match(r"^[A-Z]:$", drive):
    abort(2, "Invalid drive name.")
elif drive == "C:":
    abort(2, "Cannot operate on main drive.")

path = drive + "\\"

if not os.path.exists(path):
    abort(3, f"Drive {drive} is inaccessible.")
elif not os.access(path, os.R_OK):
    abort(5, f"You don't have permission to read from drive {drive}.")
elif not os.access(path, os.W_OK):
    abort(5, f"You don't have permission to write to drive {drive}.")

try:
    label = win32api.GetVolumeInformation(path)[0]
except:
    abort(4, "Failed to obtain drive metadata.")

SUS = [
    label,
    "USB Drive",
    "Removable Disk"
]

TRACES = [
    label + ".lnk",
    "USB Drive.lnk",
    "Removable Disk.lnk"
    "desktop.ini",
    "autorun.inf"
]

class Antivirus:
    def __init__(self):
        pass
    def exec(self):
        entity, hidden = self.check()
        if entity:
            if hidden:
                prompt("Are these (mostly) your files?")
                self.work(entity, False)
            else:
                self.work(entity, True)
        else:
            print("No threats were found by the script.")
            print(f"If you still think your drive might be infected, contact me at {email}.")
            exit(0)
    def check(self):
        print("Checking...")
        for entity in os.listdir(path):
            time.sleep(random.uniform(0.25, 2))
            if not (entity in SUS and os.path.isdir(path + entity)):
                continue
            flag = prompt(f"Should there be a directory named \"{entity}\" on your drive?")
            if flag:
                continue
            visible = bool(
                os.stat(path + entity).st_file_attributes &
                (
                    (stat.FILE_ATTRIBUTE_HIDDEN & stat.FILE_ATTRIBUTE_SYSTEM) |
                    stat.FILE_ATTRIBUTE_SYSTEM
                )
            )
            hidden = os.listdir(path + entity)
            if hidden:
                print(f"{"Hidden f" if visible else "F"}iles and/or folders found:")
                print()
                for sub in hidden:
                    print("    " + sub)
                print()
            else:
                print(f"There is an empty directory \"{entity}\" on your drive.")
            return entity, hidden
        time.sleep(random.uniform(0.5, 1.5))
        return None, None
    def work(self, entity: str, empty: bool):
        while True:
            flag = prompt(
                "Do you wish to remove the empty directory?"
                if empty else
                "Do you wish to proceed with the restoration algorithm?"
            )
            if flag:
                break
            self.stop()
        print("Working...")
        time.sleep(random.uniform(2.5, 5))
        entity_path = path + entity
        if bool(
            os.stat(entity_path).st_file_attributes &
            stat.FILE_ATTRIBUTE_SYSTEM
        ):
            os.system(f"attrib -h -s {entity_path}")
        for root, dirs, files in os.walk(path):
            for trace in TRACES:
                if trace in files:
                    full = os.path.join(root, trace)
                    if bool(
                        os.stat(full).st_file_attributes &
                        stat.FILE_ATTRIBUTE_SYSTEM
                    ):
                        os.system(f"attrib -h -s {entity_path}")
                    os.remove(full)
        for sub in os.listdir(entity_path):
            full = os.path.join(entity_path, sub)
            if bool(
                os.stat(full).st_file_attributes &
                stat.FILE_ATTRIBUTE_SYSTEM
            ):
                os.system(f"attrib -h -s {entity_path}")
            if (os.path.isdir(full)):
                shutil.copytree(full, os.path.join(path, sub))
            else:
                shutil.copy(full, path)
        shutil.rmtree(entity_path)
        print("Operation completed successfully.")
        self.after(entity, empty)
        exit(0)
    def after(self, entity: str, empty: bool):
        print("All your old files should now be in the root of your drive.")
        flag = prompt("Do you see all your files?")
        if not flag:
            print(f"Please report this bug to {email}.")
            flag = prompt("Do you wish to restart the operation?")
            self.work(entity, empty)
        else:
            flag = prompt("Do you see any unfamiliar files (e.g. \"desktop.ini\")?")
            if flag:
                print("You may safely remove any unfamiliar files.")
            flag = prompt("Is everything else intact?")
            print(f"Contact me at {email} if you need any more help.")
            print("That way you also help improve this tool.")
            if flag:
                print("Congratulations!")
                print("You have successfully restored your drive!")
    def stop(self):
        flag = prompt("Are you sure you want to abort?")
        if flag:
            print("Script aborted.")
            exit(1)
        else:
            print("Script not aborted.")

print("ANTI-RASPBERRY ROBIN 0.1.0")
print()
print()

Antivirus().exec()
