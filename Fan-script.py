import os
import time
import ipaddress
import getpass
import os
import subprocess

def clear_screen():
    os.system('clear')

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
            os.system(exit())
            return False
    except FileNotFoundError:
        print("ipmitool is not installed or not found in the PATH. Try reinstalling/installing the ipmitool package for the script to work.")
        os.system(exit())
        return False

def fan_speed():
        ip = input("Server IP: ")
        valid_ip = ipaddress.ip_address(ip)
        user = input("Username: ")
        passwd = getpass.getpass("Password: ")
        number = int(input("Enter a number from 0-100 to set the speed: "))
        assert 0 <= number <= 100, f"The number {number} is out of range!"
        hexn = hex(number)
        print(f"Your settings:\n-------------------------\nIP: {ip}\nUsername: {user}\nPassword: {passwd}\nFan-speed: {number} (hex:{hexn})\n-------------------------\n")
        sure = input("Are you sure. (y/n)").strip()
        if sure in {'y', 'Y'} or sure.lower() == 'y' or sure.upper() == 'Y':
            print(os.system(f"ipmitool -I lanplus -H {ip} -U {user} -P {passwd} raw 0x30 0x30 0x01 0x00"))
            print(os.system(f"ipmitool -I lanplus -H {ip} -U {user} -P {passwd} raw 0x30 0x30 0x02 0xff {hexn}"))
            print("Done\n ")
        else:
            print("Exit to menu\n ")

def fan_control():
    choice_input = input("0 - Manual mode\n1 - Dell auto mode\n2 - Return to menu\nEnter a number: ").strip()
    if choice_input == '2':
        print("Returning to menu...")
        return
    number = int(choice_input)
    assert 0 <= number <= 1, f"The number {number} is out of range!"
    ip = input("Server IP: ")
    valid_ip = ipaddress.ip_address(ip)
    user = input("Username: ")
    passwd = getpass.getpass("Password: ")
    print(f"Your settings:\n-------------------------\nIP: {ip}\nUsername: {user}\nPassword: {passwd}\n-------------------------\n")
    sure = input("Are you sure. (y/n)").strip()
    if sure in {'y', 'Y'} or sure.lower() == 'y' or sure.upper() == 'Y':
        if number == 0:
            print(os.system(f"ipmitool -I lanplus -H {ip} -U {user} -P {passwd} raw 0x30 0x30 0x01 0x00"))
            print("Done\n ")
        elif number == 1:
            print(os.system(f"ipmitool -I lanplus -H {ip} -U {user} -P {passwd} raw 0x30 0x30 0x01 0x01"))
            sure = input("Done.\n ")
        else:
            print("Exit to menu\n ")
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
        1: fan_control
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
    choice = input("0 - Fan speed control\n1 - Fan mode control\nExit - Quit from script\n-------------------------\nEnter item number/word: ")
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