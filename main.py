# Copyright (c) 2025 Omer Drkić
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at https://www.boost.org/LICENSE_1_0.txt)

import colorama
import ctypes
import os
import re
import shutil
import stat
import sys
import traceback
import win32api

email = colorama.Fore.LIGHTBLUE_EX + "omerdrkic2501@gmail.com" + colorama.Fore.RESET

def abort(code, string = ""):
    if string:
        sys.stderr.write(colorama.Fore.LIGHTRED_EX + string + colorama.Fore.RESET)
        sys.stderr.flush()
    os.system("@echo on")
    exit(code)

def prompt(msg):
    confirm = input(f"{msg} (Y/n) {colorama.Fore.LIGHTBLACK_EX}").lower()
    print(colorama.Fore.RESET, end="")
    while confirm not in "yn":
        confirm = input(
            f"Please enter a valid option. (Y/n) {colorama.Fore.LIGHTBLACK_EX}"
        ).lower()
        print(colorama.Fore.RESET, end="")
    return confirm == "y"

def scan(msg, conditions, reminders, common):
    data = input(f"{msg} {colorama.Fore.LIGHTBLACK_EX}").lower()
    print(colorama.Fore.RESET, end="")
    while True:
        success = True
        for i in range(len(conditions)):
            if not conditions[i](data):
                success = False
                data = input(f"{reminders[i]} {common} {colorama.Fore.LIGHTBLACK_EX}").lower()
                print(colorama.Fore.RESET, end="")
        if success:
            break
    return data

drive  = None
label  = None
sus    = None
traces = None

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
            exit()
    def check(self):
        print("Checking...")
        for entity in os.listdir(drive):
            entity_path = os.path.join(drive, entity)
            if not (entity in sus and os.path.isdir(entity_path)):
                continue
            flag = prompt(f"Should there be a directory named \"{entity}\" on your drive?")
            if flag:
                continue
            visible = bool(
                os.stat(entity_path).st_file_attributes &
                (
                    (stat.FILE_ATTRIBUTE_HIDDEN & stat.FILE_ATTRIBUTE_SYSTEM) |
                    stat.FILE_ATTRIBUTE_SYSTEM
                )
            )
            hidden = os.listdir(entity_path)
            if hidden:
                print(f"{"Hidden f" if visible else "F"}iles and/or folders found:")
                print()
                for sub in hidden:
                    print("    " + sub)
                print()
            else:
                print(f"There is an empty directory \"{entity}\" on your drive.")
            return entity, hidden
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
        dst = scan(
            "Where would you like your restored files to be?",
            [
                (lambda fp: os.path.exists(fp)),
                (lambda fp: os.path.isdir(fp)),
                (lambda fp: os.access(fp, os.R_OK)),
                (lambda fp: os.access(fp, os.W_OK)),
                (lambda fp: not os.listdir(fp))
            ],
            [
                "The provided path doesn't exist.",
                "Tho provided path isn't a directory.",
                "You don't have permission to read from the provided location.",
                "You don't have permission to write to the provided location.",
                "The directory must be empty."
            ],
            "Please enter a valid path:"
        ) if not empty else None
        print("Working...")
        entity_path = os.path.join(drive, entity)
        if bool(
            os.stat(entity_path).st_file_attributes &
            stat.FILE_ATTRIBUTE_SYSTEM
        ):
            os.system(f"attrib -h -s {entity_path}")
        for sub in os.listdir(entity_path):
            full = os.path.join(entity_path, sub)
            if bool(
                os.stat(full).st_file_attributes &
                stat.FILE_ATTRIBUTE_SYSTEM
            ):
                os.system(f"attrib -h -s {full}")
            if sub in traces:
                flag = prompt(f"Found possible malware trace file \"{sub}\". Remove?")
                if flag:
                    os.remove(full)
                    continue
            if (os.path.isdir(full)):
                shutil.copytree(full, os.path.join(dst, sub))
            else:
                shutil.copy(full, dst)
        shutil.rmtree(entity_path)
        print("Operation completed successfully.")
        self.after()
        exit()
    def after(self):
        print("All your old files should now be in the root of your drive.")
        flag = prompt("Do you see all your files?")
        if not flag:
            print(f"Please report this bug to {email} and/or try running the script again.")
            exit()
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
            exit()
        else:
            print("Script not aborted.")

def main():
    global drive, label, sus, traces
    colorama.init()
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
    if not os.path.exists(drive):
        abort(3, f"Drive {drive} is inaccessible.")
    elif not os.access(drive, os.R_OK):
        abort(5, f"You don't have permission to read from drive {drive}.")
    elif not os.access(drive, os.W_OK):
        abort(5, f"You don't have permission to write to drive {drive}.")
    try:
        label = win32api.GetVolumeInformation(drive)[0]
    except:
        abort(4, "Failed to obtain drive metadata.")
    sus = [
        label,
        "USB Drive",
        "Removable Disk"
    ]
    traces = [
        f"{label}.lnk",
        "USB Drive.lnk",
        "Removable Disk.lnk",
        "desktop.ini",
        "autorun.inf"
    ]
    print("ANTI-RASPBERRY ROBIN 0.2.0")
    print()
    print()
    try:
        Antivirus().exec()
    except:
        with open("except.log", "w+") as file:
            file.write(traceback.format_exc())
            file.close()
        print("An internal error occured.", end=" ")
        print(f"Please report this to {email} along with \"except.log\"", end=" ")
        print("which has been generated in the current working directory.")
    os.system("@echo on")

if __name__ == "__main__":
    main()
