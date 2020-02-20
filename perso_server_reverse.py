#! /usr/bin/env python3
# Les envoies se font en bytes donc on encode les str en b
import socket
import pty

hote = 'localhost'
port = 5555

connection_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#création du socket
connection_main.bind((hote, port))										#connexion du socket au serveur
connection_main.listen(5)												#mode écoute
print("The server listens on the port "+str(port))

connection_with_client, infos_connection = connection_main.accept()		#ack de connexion

msg_received = ""


while msg_received != b"end" : 											#b pour bytes
	data = ''
	while data == '':
		data = input("msg to send : ")
	connection_with_client.send(data.encode())
	msg_received = connection_with_client.recv(1024)
	print(msg_received.decode())

print ("Close of the session")
connection_with_client.close()
connection_main.close()

