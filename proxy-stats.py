#### last ran 04-12-2020 ####
import paramiko # ssh client#
import getpass
import time
import sys
import re

print("Connecting to HPNA 10.165.232.137 port 8022 enter your RSA password") 
path = (r"C:\Users\fb6erut\PycharmProjects\py-codes\ip address.txt")
proxy_IP = open(path, 'r')

output_file = open(r"C:\Users\fb6erut\PycharmProjects\py-codes\test-hpna-proxy-stats.txt", 'wb') ## open file to write contents to this##

ip = '10.165.232.137'
username = 'fb6erut'
password = getpass.getpass()
ssh_conn = paramiko.SSHClient()
ssh_conn.set_missing_host_key_policy (paramiko.AutoAddPolicy())
ssh_conn.connect(ip, port=8022, username=username, password=password, look_for_keys=False, allow_agent=False)
ssh_conn =  ssh_conn.invoke_shell()
time.sleep(5)
output = ssh_conn.recv(1000)
print(output.decode(), end = '')

print("logged on to HPNA cli....reading from file...connecting to proxies through HPNA")
time.sleep(3)
#connects to proxy & return the output. 
def Connect_to_proxy(): 
	for IP in proxy_IP:
		IP = IP.strip()

		# print(IP)
		time.sleep(2)
		ssh_conn.send("connect " + IP + "\n")
		time.sleep(2)
		ssh_conn.send("\n")
		output = ssh_conn.recv(1000)
		print(output.decode(), end = '' )
		time.sleep(1)
		ssh_conn.send("show status \n")
		time.sleep(1)
		cmd_output = ssh_conn.recv(1000)
		output_file.write(cmd_output)
		ssh_conn.send("show ntp \n")
		time.sleep(1)
		cmd_output = ssh_conn.recv(1000)
		# print(cmd_output.decode(), end = ' ') uncomment this line in order to see output on screen
		output_file.write(cmd_output)
		ssh_conn.send("exit\n")
		time.sleep(1)
		output = ssh_conn.recv(1000)
		print(output.decode(), end=" ")
		print(output.decode(), end=" ")

Connect_to_proxy()

proxy_IP.close()
output_file.close() # closing the file #
ssh_conn.close()
print("Completed command execution for all the proxies")
time.sleep(3)
def regex_compliation():
	path = (r"C:\Users\fb6erut\PycharmProjects\py-codes\test-hpna-proxy-stats.txt")
	f = open(path)
	f.seek(0)
	contents = f.read()

	match_names = re.findall(r"Name:\s+(.+?)\n", contents)
     
	match_serials = re.findall(r"Serial number:\s+(.+?)\n", contents)
     
	match_times = re.findall(r"System started:\s+(.+?)\n", contents)
	print("\nOutput of Name, serial number and Start time")
	for index, name in enumerate(match_names):
		print("Name: " + name, end = "\n")
		print("Serial Number: " + match_serials[index], end = "\n")
		print("System start time: " + match_times[index], end = "\n\n")
		
regex_compliation()		