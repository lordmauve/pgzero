#!/usr/bin/env python3
"""Update the SDL controller DB files for automatic controller mapping in
Pygame Zero.

The source file is retrieved from the repo and the platform specific
mappings extracted into three separate files in src/pgzero/data.

"""
import requests

DEST = "./src/pgzero/data/"
REPO_URL = ("https://raw.githubusercontent.com/mdqinc/SDL_GameControllerDB"
            "/refs/heads/master/gamecontrollerdb.txt")

data = requests.get(REPO_URL)
text_lines = data.text.splitlines()
print("Gotten data.")

lines = iter(text_lines)
line = next(lines)

while "# Windows" not in line:
    line = next(lines)
line = next(lines)

with open(DEST + "controllers_windows.txt", "w") as outfile:
    while line != "":
        outfile.write(line + "\n")
        line = next(lines)

print("Written Windows mappings.")

next(lines)
line = next(lines)

with open(DEST + "controllers_macos.txt", "w") as outfile:
    while line != "":
        outfile.write(line + "\n")
        line = next(lines)

print("Written MacOS mappings.")

next(lines)
line = next(lines)

with open(DEST + "controllers_linux.txt", "w") as outfile:
    while line != "":
        outfile.write(line + "\n")
        line = next(lines)

print("Written Linux mappings.")

print("Finished writing all controllers mappings, exiting.")
