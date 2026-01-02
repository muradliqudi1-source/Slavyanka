import os 
import sys
import json
import requests
import random
import subprocess

logo = """
                                                                                                                                                                           
                                                                                                                                                              
                 lllllll                                                                                                   kkkkkkkk                           
                 l:::::l                                                                                                   k::::::k                           
                 l:::::l                                                                                                   k::::::k                           
                 l:::::l                                                                                                   k::::::k                           
    ssssssssss    l::::l   aaaaaaaaaaaaavvvvvvv           vvvvvvvyyyyyyy           yyyyyyyaaaaaaaaaaaaa  nnnn  nnnnnnnn     k:::::k    kkkkkkkaaaaaaaaaaaaa   
  ss::::::::::s   l::::l   a::::::::::::av:::::v         v:::::v  y:::::y         y:::::y a::::::::::::a n:::nn::::::::nn   k:::::k   k:::::k a::::::::::::a  
ss:::::::::::::s  l::::l   aaaaaaaaa:::::av:::::v       v:::::v    y:::::y       y:::::y  aaaaaaaaa:::::an::::::::::::::nn  k:::::k  k:::::k  aaaaaaaaa:::::a 
s::::::ssss:::::s l::::l            a::::a v:::::v     v:::::v      y:::::y     y:::::y            a::::ann:::::::::::::::n k:::::k k:::::k            a::::a 
 s:::::s  ssssss  l::::l     aaaaaaa:::::a  v:::::v   v:::::v        y:::::y   y:::::y      aaaaaaa:::::a  n:::::nnnn:::::n k::::::k:::::k      aaaaaaa:::::a 
   s::::::s       l::::l   aa::::::::::::a   v:::::v v:::::v          y:::::y y:::::y     aa::::::::::::a  n::::n    n::::n k:::::::::::k     aa::::::::::::a 
      s::::::s    l::::l  a::::aaaa::::::a    v:::::v:::::v            y:::::y:::::y     a::::aaaa::::::a  n::::n    n::::n k:::::::::::k    a::::aaaa::::::a 
ssssss   s:::::s  l::::l a::::a    a:::::a     v:::::::::v              y:::::::::y     a::::a    a:::::a  n::::n    n::::n k::::::k:::::k  a::::a    a:::::a 
s:::::ssss::::::sl::::::la::::a    a:::::a      v:::::::v                y:::::::y      a::::a    a:::::a  n::::n    n::::nk::::::k k:::::k a::::a    a:::::a 
s::::::::::::::s l::::::la:::::aaaa::::::a       v:::::v                  y:::::y       a:::::aaaa::::::a  n::::n    n::::nk::::::k  k:::::ka:::::aaaa::::::a 
 s:::::::::::ss  l::::::l a::::::::::aa:::a       v:::v                  y:::::y         a::::::::::aa:::a n::::n    n::::nk::::::k   k:::::ka::::::::::aa:::a
  sssssssssss    llllllll  aaaaaaaaaa  aaaa        vvv                  y:::::y           aaaaaaaaaa  aaaa nnnnnn    nnnnnnkkkkkkkk    kkkkkkkaaaaaaaaaa  aaaa
                                                                       y:::::y                                                                                
                                                                      y:::::y                                                                                 
                                                                     y:::::y                                                                                  
                                                                    y:::::y                                                                                   
                                                                   yyyyyyy                                                                                    
                                                                                                                                                              
"""               
colors = [
    "\033[31m",  # red
    "\033[32m",  # green
    "\033[33m",  # yellow
    "\033[34m",  # blue
    "\033[35m",  # magenta
    "\033[36m",  # cyan
    "\033[37m",  # white
]



for line in logo.splitlines():
    color = random.choice(colors)
    print(f"{color}{line}")    
while True:
    print("\033[0m")  # Reset color
    print("1. IP Lookup")
    print("2. Camera Capture Server")
    print("3. Location Server")
    print("4. Voice Recorder Server")
    print("5. Username OSINT (30+ sites)")
    print("6. Exit")
    choice = input("Select an option: ")
    if choice == '1':
        ip = input("Enter Your IP: ")
        if not ip:
            print("IP address is required!")
            continue
        url = f"http://ip-api.com/json/{ip}"
        data = requests.get(url).json()
        print("IP:", data.get("query"))
        print("Country:", data.get("country"))
        print("City:", data.get("city"))
        print("ISP:", data.get("isp"))
        print("Status:", data.get("status"))
    elif choice == '2':
        os.system('python camera_server.py')
    elif choice == '3':
        os.system('python location_server.py')
    elif choice == '4':
        os.system('python voice_server.py')
    elif choice == '5':
        os.system('python username_osint.py')
    elif choice == '6':
        break
