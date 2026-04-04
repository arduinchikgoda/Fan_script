import os
import time
import ipaddress
import getpass
import subprocess
import json

def auth_file():
    default_config = "data.json"
    folder = input("Enter folder name (leave empty for current): ").strip()
    filename = input(f"Enter filename [default - {default_config}]:  ").strip() or "data"
    if not filename.endswith(".json"):
        filename += ".json"
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        confirm = input(f"File '{filename}' already exists. Overwrite? (y/n): ").lower().strip()
        if confirm != 'y':
            print("Saving cancelled.")
            return 
    data = {
        "ip": input("Server IP: ").strip(),
        "user": input("Username: ").strip(),
        "passwd": input("Password: ").strip()
    }

    try:
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"File successfully saved at: {os.path.abspath(path)}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return

def clear_screen():
    subprocess.run(["clear"])

def check_ipmitool():
    try:
        result = subprocess.run(['ipmitool', '-V'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            print(f"ipmitool is installed: {result.stdout.strip()}")
            return True
        else:
            print("ipmitool was not found (execution error). Try reinstalling/installing the ipmitool package for the script to work.")
            exit()
            return False
    except FileNotFoundError:
        print("ipmitool is not installed or not found in the PATH. Try reinstalling/installing the ipmitool package for the script to work.")
        exit()
        return False

def fan_speed():
    default_config = "data.json"
    user_path = input(f"Enter the path to the JSON file [default - {default_config}]: ").strip()
    config_file = user_path if user_path else default_config
    ip, user, passwd = None, None, None
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ip = data.get('ip')
                user = data.get('user')
                passwd = data.get('passwd')
                print(f"Data loaded from: {config_file}")
        except Exception as e:
            print(f"Error reading file: {e}")

    if not all([ip, user, passwd]):
        if os.path.exists(config_file):
            print("The file was found, but some data is missing. Please fill it in:")
        else:
            print(f"File '{config_file}' not found. Please enter the information manually:")
        ip = ip or input("Server IP: ")
        user = user or input("Username: ")
        passwd = passwd or getpass.getpass("Password: ")
    try:
        ipaddress.ip_address(ip)
        number = int(input("Enter a number from 0-100 to set the speed: "))
        assert 0 <= number <= 100, f"The number {number} is out of range!"
        hexn = hex(number)
        print(f"Your settings:\n-------------------------\nIP: {ip}\nUsername: {user}\nPassword: {passwd}\nFan-speed: {number} (hex:{hexn})\n-------------------------")
        sure = input("Are you sure. (y/n)").strip()
        if sure in {'y', 'Y'} or sure.lower() == 'y' or sure.upper() == 'Y':
            try:
                subprocess.run(["ipmitool", "-I", "lanplus", "-H", ip, "-U", user, "-P", passwd, "raw", "0x30", "0x30", "0x01", "0x00"], capture_output=True, text=True, check=True)
                subprocess.run(["ipmitool", "-I", "lanplus", "-H", ip, "-U", user, "-P", passwd, "raw", "0x30", "0x30", "0x02", "0xff", hexn], capture_output=True, text=True)
                print("Done. Returning to menu...")
            except subprocess.CalledProcessError:
                print(f"Failed with return code {e}")
        else:
            print("Cancelled\n")
    except Exception as e:
        print(f"An unexpected error occurred {e}")

def fan_control():
    choice_input = input("0 - Manual mode\n1 - Dell auto mode\n2 - Return to menu\nEnter a number: ").strip()
    if choice_input == '2':
        print("Returning to menu...")
        return
    number = int(choice_input)
    assert 0 <= number <= 1, f"The number {number} is out of range!"
    default_config = "data.json"
    user_path = input(f"Enter path to JSON file [default: {default_config}]: ").strip()
    config_file = user_path if user_path else default_config
    ip, user, passwd = None, None, None
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ip = data.get('ip')
                user = data.get('user')
                passwd = data.get('passwd')
                print(f"Data loaded from: {config_file}")
        except Exception as e:
            print(f"Error reading file: {e}")
    if not all([ip, user, passwd]):
        if os.path.exists(config_file):
            print("The file was found, but some data is missing. Please fill it in:")
        else:
            print(f"File '{config_file}' not found. Please enter the information manually:")
        ip = ip or input("Server IP: ")
        user = user or input("Username: ")
        passwd = passwd or getpass.getpass("Password: ")
    print(f"Your settings:\n-------------------------\nIP: {ip}\nUsername: {user}\nPassword: {passwd}\n-------------------------\n")
    sure = input("Are you sure. (y/n)").strip()
    if sure in {'y', 'Y'} or sure.lower() == 'y' or sure.upper() == 'Y':
        if number == 0:
            try:
                subprocess.run(["ipmitool", "-I", "lanplus", "-H", ip, "-U", user, "-P", passwd, "raw", "0x30", "0x30", "0x01", "0x00"], capture_output=True, text=True, check=True)
                print("Done\n ")
            except subprocess.CalledProcessError:
                print(f"Failed with return code {e}")
        elif number == 1:
            try:
                subprocess.run(["ipmitool", "-I", "lanplus", "-H", ip, "-U", user, "-P", passwd, "raw", "0x30", "0x30", "0x01", "0x01"], capture_output=True, text=True, check=True)
                print("Done\n ")
            except subprocess.CalledProcessError:
                print(f"Failed with return code {e}")
    else:
        print("Exit to menu\n ")

def print_gradient_logo(text):
    lines = text.strip("\n").splitlines()
    steps = len(lines)
    
    for i, line in enumerate(lines):
        r = int(255 - (i * (255 / (steps - 1))))
        g = 0
        b = int(i * (255 / (steps - 1)))
        color_code = f"\033[1;38;2;{r};{g};{b}m"
        reset_code = "\033[0m"
        print(f"{color_code}{line}{reset_code}")


commands = {
        0: fan_speed,
        1: fan_control,
        2: auth_file
    }

LOGO = (r"""
 $$$$$$$$\                                                     $$\            $$\     
$$  _____|                                                    \__|           $$ |    
$$ |   $$$$$$\  $$$$$$$\         $$$$$$$\  $$$$$$$\  $$$$$$\  $$\  $$$$$$\ $$$$$$\   
$$$$$\ \____$$\ $$  __$$\       $$  _____|$$  _____|$$  __$$\ $$ |$$  __$$\\_$$  _|  
$$  __|$$$$$$$ |$$ |  $$ |      \$$$$$$\  $$ /      $$ |  \__|$$ |$$ /  $$ | $$ |    
$$ |  $$  __$$ |$$ |  $$ |       \____$$\ $$ |      $$ |      $$ |$$ |  $$ | $$ |$$\ 
$$ |  \$$$$$$$ |$$ |  $$ |      $$$$$$$  |\$$$$$$$\ $$ |      $$ |$$$$$$$  | \$$$$  |
\__|   \_______|\__|  \__|      \_______/  \_______|\__|      \__|$$  ____/   \____/ 
                                                                  $$ |               
                                                                  $$ |               
                                                                  \__|
    """)
def main():
    print("\033[1;31mWARNING: Use at your own risk. This software allows you to manually control the server fan speed.\033[0m\n-------------------------")
    choice = input("0 - Fan speed control\n1 - Fan mode control\n2 - Add or edit IPMI auth file\nExit - Quit from script\n-------------------------\nEnter item number/word: ")
    if choice.lower() == 'exit':
        print("Exiting the fan-script")
        time.sleep(1)
        exit()
    if choice.isdigit():
        choice_int = int(choice)
        if choice_int in commands:
            commands[choice_int]()
    else:
        print("No command. Try again\n ")

if __name__ == "__main__":
    check_ipmitool()
    while True:
        try:
            time.sleep(4)
            clear_screen()
            print_gradient_logo(LOGO)
            running = main()
        except ValueError:
            print("Error: You entered an invalid input! Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred ({type(e).__name__}): {e}")
        except KeyboardInterrupt:
            print("\nFan-script was stopped by the user.")
            break