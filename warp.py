import json
import datetime
import random
import string
import threading

try:
    import httpx
except ImportError:
    print("httpx package not found. Installing...")
    os.system("pip install httpx")
    import httpx

# Define script version and window title
script_version = '4.4.1'

# Print information about the script (without your name and website)
print("[+] ABOUT SCRIPT:")
print("[-] With this script, you can obtain unlimited WARP+ referral data.")
print(f"[-] Version: {script_version}")
print("[♡] Made with ♡ by Navaneeth K M (nxvvvv)")
print("--------")

# Initialize user settings
referrer = ""
save_file = "warp.sav"
stop_flag = False

# Load referral data and saved client IDs from script data structures
referral_data = {
    "users": {},
    "total": {
        "total_referrals": 0
    }
}

# Function to generate a random string
def genString(stringLength):
    try:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(stringLength))
    except Exception as error:
        print(error)

# Function to generate a random digit string
def digitString(stringLength):
    try:
        digit = string.digits
        return ''.join(random.choice(digit) for _ in range(stringLength))
    except Exception as error:
        print(error)

# Define the API URL
url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'

# Function to send a request to the API and handle the response
def run():
    global stop_flag
    try:
        install_id = genString(22)
        body = {
            "key": f"{genString(43)}=",
            "install_id": install_id,
            "fcm_token": f"{install_id}:APA91b{genString(134)}",
            "referrer": referrer,
            "warp_enabled": False,
            "tos": f"{datetime.datetime.now().isoformat()[:-3]}+02:00",
            "type": "Android",
            "locale": "es_ES",
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'api.cloudflareclient.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'
        }

        with httpx.Client() as client:
            response = client.post(url, json=body, headers=headers)

        if response.status_code == 200:
            print(f"\n[-] WORK ON ID: {referrer}")
            print(f"[:)] Request completed successfully.")
            return True
        else:
            print("[:(] Error when connecting to server.")
            return False
    except Exception as error:
        print("")
        print(error)
        return False

# Function to send requests concurrently
def send_requests():
    global stop_flag

    while not stop_flag:
        result = run()
        if result:
            if referrer in referral_data["users"]:
                referral_data["users"][referrer][1] += 10  # Increment successful referrals by 10GB
            else:
                referral_data["users"][referrer] = [referrer, 10]  # Initialize successful referrals to 10GB
            referral_data["total"]["total_referrals"] += 10  # Increment total successful referrals by 10GB
            update_log_file()
            print(f"[:)] Request completed.")
            # Check if we have reached 1000 successful referrals (1000 * 10GB = 10,000GB)
            if referral_data["total"]["total_referrals"] >= 1000:
                stop_flag = True
                print("[!] Reached 1000 successful referrals (10,000GB). Stopping the script...")
        else:
            print("\n[:(] Error when connecting to server.")

# Function to update the log file with referral data
def update_log_file():
    global referral_data
    with open(save_file, "w") as log_file:
        json.dump(referral_data, log_file, indent=2)

# Function to check for the 's' key press to stop the script
def check_stop_key():
    global stop_flag
    while True:
        if input("Press 's' and Enter to stop the script: ").strip().lower() == 's':
            stop_flag = True
            print("\n[!] Stopping the script...")
            break

# Main script loop
while True:
    print("\n[+] MENU:")
    print("1. Start Script")
    print("2. Set Referrer (User ID)")
    print("3. Display Referral Data")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        if not referrer:
            referrer = input("Enter the Referrer (User ID): ")
        stop_flag = False  # Reset the stop flag
        # Start the thread to send requests concurrently
        request_thread = threading.Thread(target=send_requests)
        request_thread.start()
    elif choice == '2':
        referrer = input("Enter the Referrer (User ID): ")
    elif choice == '3':
        print("Referral Data:")
        print(json.dumps(referral_data, indent=2))
    elif choice == '4':
        print("[+] Exiting the script.")
        stop_flag = True  # Set the stop flag to stop the request thread
        # Wait for the request thread to finish
        request_thread.join()
        break
    else:
        print("[!] Invalid choice. Please select a valid option.")
