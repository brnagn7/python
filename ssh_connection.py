#!/usr/bin/python
import getopt, sys, paramiko, getpass

#
# filename:	ssh_connection.py
# author:	ed mooney
# date:		April 2017
# desc:		connects to router/switch and performs task
#		then writes result to a file
#
# todo:		Truly amazing things
#

# variables
ip = raw_input('IP Address:  ')
username = raw_input('Username:  ')
password = getpass.getpass('Password: ')
command = raw_input('Command: ')

#
# main task function
# connects to router/switch
# performs task given
# writes to file
#
def connect_to(ip):
			task = command.rstrip()
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
			stdin, stdout, stderr = ssh.exec_command(task)
			output = open(ip + ".out", "a")
			output.write("\n\nCommand Issued: "+task+"\n")
			output.writelines(stdout)
			output.write("\n")
			print "Your file has been updated, it is ", ip+".out"
			ssh.close()
connect_to(ip)
#END
