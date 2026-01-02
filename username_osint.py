import requests
import os
import concurrent.futures
from colorama import init, Fore, Style

init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# List of sites to check: (name, url_template, expected_status_for_exists)
# Some sites return 200 even for non-existent users, so we check response content
SITES = [
    ("Instagram", "https://www.instagram.com/{}/", 200),
    ("Twitter/X", "https://twitter.com/{}", 200),
    ("TikTok", "https://www.tiktok.com/@{}", 200),
    ("GitHub", "https://github.com/{}", 200),
    ("Reddit", "https://www.reddit.com/user/{}", 200),
    ("YouTube", "https://www.youtube.com/@{}", 200),
    ("Pinterest", "https://www.pinterest.com/{}/", 200),
    ("Tumblr", "https://{}.tumblr.com", 200),
    ("Medium", "https://medium.com/@{}", 200),
    ("Twitch", "https://www.twitch.tv/{}", 200),
    ("Spotify", "https://open.spotify.com/user/{}", 200),
    ("SoundCloud", "https://soundcloud.com/{}", 200),
    ("VK", "https://vk.com/{}", 200),
    ("Flickr", "https://www.flickr.com/people/{}", 200),
    ("Steam", "https://steamcommunity.com/id/{}", 200),
    ("DeviantArt", "https://www.deviantart.com/{}", 200),
    ("Dribbble", "https://dribbble.com/{}", 200),
    ("Behance", "https://www.behance.net/{}", 200),
    ("GitLab", "https://gitlab.com/{}", 200),
    ("BitBucket", "https://bitbucket.org/{}/", 200),
    ("Patreon", "https://www.patreon.com/{}", 200),
    ("LinkedIn", "https://www.linkedin.com/in/{}", 200),
    ("Facebook", "https://www.facebook.com/{}", 200),
    ("Snapchat", "https://www.snapchat.com/add/{}", 200),
    ("Telegram", "https://t.me/{}", 200),
    ("Discord (Server)", "https://discord.com/invite/{}", 200),
    ("Roblox", "https://www.roblox.com/users/profile?username={}", 200),
    ("Minecraft (NameMC)", "https://namemc.com/profile/{}", 200),
    ("Chess.com", "https://www.chess.com/member/{}", 200),
    ("Replit", "https://replit.com/@{}", 200),
    ("HackerRank", "https://www.hackerrank.com/{}", 200),
    ("LeetCode", "https://leetcode.com/{}", 200),
    ("Keybase", "https://keybase.io/{}", 200),
    ("About.me", "https://about.me/{}", 200),
    ("Gravatar", "https://en.gravatar.com/{}", 200),
]

def check_site(site_info, username):
    name, url_template, expected_status = site_info
    url = url_template.format(username)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        # Check if account exists
        if response.status_code == 200:
            # Some sites return 200 but show "not found" in content
            # We do a basic check for common "not found" patterns
            content_lower = response.text.lower()
            not_found_indicators = [
                "page not found",
                "user not found", 
                "this page isn't available",
                "sorry, this page",
                "doesn't exist",
                "couldn't find",
                "no user",
                "404"
            ]
            
            for indicator in not_found_indicators:
                if indicator in content_lower:
                    return (name, url, False)
            
            return (name, url, True)
        elif response.status_code == 404:
            return (name, url, False)
        else:
            return (name, url, None)  # Unknown/blocked
            
    except requests.exceptions.Timeout:
        return (name, url, None)
    except requests.exceptions.RequestException:
        return (name, url, None)

def main():
    clear()
    print(f"""{Fore.CYAN}
  _   _                                            ___  ____ ___ _   _ _____ 
 | | | |___  ___ _ __ _ __   __ _ _ __ ___   ___  / _ \/ ___|_ _| \ | |_   _|
 | | | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \ / _ \| | | \___ \| ||  \| | | |  
 | |_| \__ \  __/ |  | | | | (_| | | | | | |  __/| |_| |___) | || |\  | | |  
  \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___| \___/|____/___|_| \_| |_|  
                                                                             
    {Fore.YELLOW}Find usernames across 30+ platforms
    {Style.RESET_ALL}""")
    
    username = input(f"{Fore.GREEN}[?] Enter username to search: {Style.RESET_ALL}").strip()
    
    if not username:
        print(f"{Fore.RED}Username is required!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}[*] Searching for '{username}' across {len(SITES)} platforms...{Style.RESET_ALL}\n")
    
    found = []
    not_found = []
    errors = []
    
    # Use threading for faster checks
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(check_site, site, username): site for site in SITES}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            name, url, exists = result
            
            if exists == True:
                found.append((name, url))
                print(f"{Fore.GREEN}[+] FOUND: {name:<20} {url}{Style.RESET_ALL}")
            elif exists == False:
                not_found.append(name)
            else:
                errors.append(name)
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Found on {len(found)} platforms{Style.RESET_ALL}")
    print(f"{Fore.RED}[-] Not found on {len(not_found)} platforms{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[?] Error/blocked on {len(errors)} platforms{Style.RESET_ALL}")
    
    if found:
        print(f"\n{Fore.CYAN}[*] Direct Links:{Style.RESET_ALL}")
        for name, url in found:
            print(f"    {Fore.GREEN}{name}: {url}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
