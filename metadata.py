from PIL import Image, ExifTags
import sys
import os
from colorama import init, Fore, Style

init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    if ref in ['S', 'W']:
        decimal = -decimal
        
    return decimal

def get_coordinates(gps_info):
    lat = None
    lon = None
    
    # GPS Latitude codes: 2 (Lat), 1 (Ref N/S)
    # GPS Longitude codes: 4 (Long), 3 (Ref E/W)
    
    if 2 in gps_info and 1 in gps_info:
        lat = get_decimal_from_dms(gps_info[2], gps_info[1])
        
    if 4 in gps_info and 3 in gps_info:
        lon = get_decimal_from_dms(gps_info[4], gps_info[3])
        
    return lat, lon

def main():
    clear()
    print(f"""{Fore.CYAN}
  __  __ ______ _______          _____         _______       
 |  \/  |  ____|__   __|   /\   |  __ \     /\|__   __|/\    
 | \  / | |__     | |     /  \  | |  | |   /  \  | |  /  \   
 | |\/| |  __|    | |    / /\ \ | |  | |  / /\ \ | | / /\ \  
 | |  | | |____   | |   / ____ \| |__| | / ____ \| |/ ____ \ 
 |_|  |_|______|  |_|  /_/    \_\_____/ /_/    \_\_/_/    \_\\
                                                             
    {Fore.YELLOW}Image Exif Data Extractor
    {Style.RESET_ALL}""")

    image_path = input(f"{Fore.GREEN}[?] Enter path to image (drag & drop file here): {Style.RESET_ALL}").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"{Fore.RED}[!] File not found.{Style.RESET_ALL}")
        return

    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if not exif_data:
            print(f"{Fore.RED}[!] No Exif data found in this image.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Note: Social media (WhatsApp, Instagram, Telegram) automatically removes Exif data for privacy.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}[*] Extracting Metadata...{Style.RESET_ALL}\n")
        
        gps_info = {}

        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            
            # Filter long binary data
            if isinstance(value, bytes) and len(value) > 50:
                value = "(Binary Data)"
                
            if tag_name == "GPSInfo":
                gps_info = value
                continue # Handle GPS separately
                
            print(f"{Fore.GREEN}{tag_name:<25}{Style.RESET_ALL}: {value}")

        # Handle GPS
        if gps_info:
            print(f"\n{Fore.YELLOW}[*] GPS INFO FOUND!{Style.RESET_ALL}")
            lat, lon = get_coordinates(gps_info)
            
            if lat and lon:
                print(f"{Fore.MAGENTA}Latitude : {lat}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Longitude: {lon}{Style.RESET_ALL}")
                
                maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                print(f"\n{Fore.CYAN}[GOOGLE MAPS LINK]{Style.RESET_ALL}")
                print(f"{Fore.BLUE}{maps_url}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Could not parse coordinates.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[!] No GPS Info found in this image.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
