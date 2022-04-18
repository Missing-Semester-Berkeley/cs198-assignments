import socket
import sys
import os
# https://docs.python.org/3/howto/sockets.html

port = int(os.environ.get("PORT", 8080))

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("localhost", port))
serversocket.listen(1)

TAG_LEN = 3
NAME_LENGTH = 4
POS_LENGTH = 1
TAG_LENS = {
        "GLI": 0,
        "ADD": 1 + NAME_LENGTH,  # Space + Name
        "AAP": 1 + NAME_LENGTH + 1 + POS_LENGTH,
        "RMV": 1 + NAME_LENGTH,
        "UPD": 1 + NAME_LENGTH + 1 + POS_LENGTH,
        "GET": 1 + NAME_LENGTH,
        "EXT": 0,
}

queue = ["LEVI"]  # For testing purposes, we start the queue with 1 person.

while True:
    (clientsocket, address) = serversocket.accept()

    while True:  # Each iteration of loop handles one message
        buffer = ""
        message_to_send = None
        while len(buffer) < TAG_LEN:  # Wait until tag is received
            buffer += clientsocket.recv(2048).decode()

        tag, buffer = buffer[:TAG_LEN], buffer[TAG_LEN:]

        print("DEBUG[server][TAG]:", tag)

        while len(buffer) < TAG_LENS[tag]:  # Wait until full message is received
            buffer += clientsocket.recv(2048).decode()

        print("DEBUG[server][BUFFER]:", buffer)

        # `buffer` now contains the parts of the message you want. For example, with
        #     `ADD NAME POS`
        # `buffer` now contains
        #     ` NAME POS`
        # Don't forget to take out the leading space!

        # To send a message, set the variable `message_to_send`. It will
        # send at the end of the loop (see last two lines.)

        if tag == "GLI":
            """Implement Question 1"""
        elif tag == "ADD":
            """Implement Question 2"""
        elif tag == "AAP":
            """Implement Question 3"""
        elif tag == "RMV":
            """Implement Question 4"""
        elif tag == "UPD":
            """Implement Question 5"""
        elif tag == "GET":
            """Implement Question 6"""
        elif tag == "EXT":
            clientsocket.close()
            sys.exit(0)

        if message_to_send is not None:
            print("DEBUG[server][SENDING]:", message_to_send)
            clientsocket.send(message_to_send.encode())
