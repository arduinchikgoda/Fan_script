# Fan-script
## A script for fan management for Dell Poweredge servers. The script should work from the 11th generation of servers to the 13th (Tested on Dell Poweredge R620, BIOS version 2.9.0. IDRAC version 7).
![](/example.png)


**WARNING: Use at your own risk. This software allows you to manually control the server fan speed.**

**ipmitool is _required_ for the script to work.**

Debian / Ubuntu / Mint / Kali:
```
sudo apt update
sudo apt install ipmitool
```
RHEL / CentOS / Fedora / AlmaLinux / Rocky Linux:
```
sudo yum install OpenIPMI ipmitool
# OR
sudo dnf install OpenIPMI ipmitool
```
Arch Linux / Manjaro:
```
sudo pacman -S ipmitool
```
SUSE / openSUSE:
```
sudo zypper install ipmitool
```
Checking the installation:
```
ipmitool -V
```
