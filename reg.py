import requests
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Registration URL
url = "https://app.blockmesh.xyz/register"

# Request headers
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://app.blockmesh.xyz",
    "Referer": "https://app.blockmesh.xyz/register?invite_code=runcode",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

# Log file for successful registrations
success_log_file = "success_log.txt"

# Encrypted invite code
encrypted_code = base64.b64encode(b'runcode').decode('utf-8')

def get_invite_code():
    return base64.b64decode(encrypted_code).decode('utf-8')

# Read .txt file and attempt registration
try:
    logging.debug("Attempting to open accounts.txt file")
    with open("accounts.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        if not lines:
            logging.critical("accounts.txt file is empty")
        else:
            logging.debug(f"Read {len(lines)} lines from accounts.txt")
        
        for line in lines:
            line = line.strip()
            if not line:
                logging.debug("Skipping empty line")
                continue

            logging.debug(f"Reading line: {line}")
            try:
                email, password = line.split(",")
                logging.debug(f"Parsed email: {email}, password: {password}")
            except ValueError:
                logging.warning("Line format is incorrect, skipping this line")
                continue

            data = {
                "email": email,
                "password": password,
                "password_confirm": password,
                "invite_code": get_invite_code()
            }

            try:
                logging.debug(f"Starting registration for: {email}")
                response = requests.post(url, headers=headers, data=data, allow_redirects=True)
                logging.debug(f"Status code: {response.status_code}")
                logging.debug(f"Response content: {response.text}")
                
                if response.status_code == 200:
                    logging.info(f"Registration successful: {email}")
                    with open(success_log_file, "a", encoding="utf-8") as success_file:
                        success_file.write(f"{email},{password}\n")
                elif response.status_code == 303:
                    logging.info(f"Redirect URL: {response.headers.get('Location')}")
                else:
                    logging.error(f"Registration failed for: {email}, Error: {response.text}")
            except requests.RequestException as e:
                logging.error(f"Request error: {e}")

except FileNotFoundError:
    logging.critical("accounts.txt file not found. Please ensure the file exists in the script directory.")
except Exception as e:
    logging.critical(f"Error reading file: {e}")
