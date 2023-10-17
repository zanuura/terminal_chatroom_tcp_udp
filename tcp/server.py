import socket
import threading

host = '127.0.0.1'
port = 55555

# start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        print("Server is running and Listening...")
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send("Connected to server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client))
        thread.start()


if __name__ == "__main__":
    receive()
