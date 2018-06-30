
import socket
import json
import keyboard

 
#TCP_IP = '127.0.0.1'
TCP_PORT = 6624
BUFFER_SIZE = 512

#magic socket stuff
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), TCP_PORT))
s.listen(1)
 
conn, addr = s.accept()

print('Connection address:', addr)

while True:
    send_this_shit = {'W':False,'A':False,'S':False,'D':False}
    data = conn.recv(BUFFER_SIZE)
    #print(data)

    #if not data: break

    if keyboard.is_pressed('w'):
        send_this_shit.update({'W':True})
    if keyboard.is_pressed('a'):
        send_this_shit.update({'A':True})
    if keyboard.is_pressed('s'):
        send_this_shit.update({'S':True})
    if keyboard.is_pressed('d'):
        send_this_shit.update({'D':True})

    print(json.dumps(send_this_shit))
    conn.send(json.dumps(send_this_shit).encode())  # send data

conn.close()
