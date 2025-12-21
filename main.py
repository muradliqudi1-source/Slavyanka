import json
import os
import requests
logo = """
▄█    █▄     ▄██████▄   ▄█         ▄▄▄▄███▄▄▄▄    ▄█  ███    █▄    ▄▄▄▄███▄▄▄▄
███    ███   ███    ███ ███       ▄██▀▀▀███▀▀▀██▄ ███  ███    ███ ▄██▀▀▀███▀▀▀██▄
███    ███   ███    ███ ███       ███   ███   ███ ███▌ ███    ███ ███   ███   ███
███▄▄▄▄███▄▄ ███    ███ ███       ███   ███   ███ ███▌ ███    ███ ███   ███   ███
███▀▀▀▀███▀  ███    ███ ███       ███   ███   ███ ███▌ ███    ███ ███   ███   ███
███    ███   ███    ███ ███       ███   ███   ███ ███  ███    ███ ███   ███   ███
███    ███   ███    ███ ███▌    ▄ ███   ███   ███ ███  ███    ███ ███   ███   ███
███    █▀     ▀██████▀  █████▄▄██  ▀█   ███   █▀  █▀   ████████▀   ▀█   ███   █▀
"""
colors = [
    (255, 0, 255),    # magenta
    (0, 120, 255),    # blue
    (255, 60, 60),    # red
    (165, 42, 42),    # brown
    (180, 0, 255),    # purple
    (0, 200, 150),
    (255, 180, 0),
    (120, 255, 120)
]

for i, line in enumerate(logo.splitlines()):
    r, g, b = colors[i % len(colors)]
    print(f"\033[38;2;{r};{g};{b}m{line}\033[0m")

print ("67.Element Holmium du ordan bele havali panel cixardim - Slavyanka Sad Boy")

print ("1)Surprise Eger baxirsansa :( onsuz baxan olmazda ins :D")
x=input ("Well 1 opsiyon var sec : ")
if x =="1":
     print("Ss gonder mene sene surprise edim :D sad boy ")
    
