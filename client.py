# Python program to implement client side of chat room.
import socket
import select
import sys

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # if len(sys.argv) != 3:
    # 	print ("Correct usage: script, IP address, port number")
    # 	exit()
    UserName = input("Your username: ")
    IP_address = str('127.0.0.1')
    Port = 8080
    server.connect((IP_address, Port))
    isRunning=True

    message = server.recv(1024).decode()
    print("1",message)
    isUsers = server.recv(1024).decode()
    if isUsers=="True":
        server.setblocking(False)

    while isRunning:
        try:
            sockets_list = [sys.stdin, server]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == server:
                    if isUsers == "False":
                        message = server.recv(1024).decode()
                        if message:
                            isUsers = "True"
                            server.setblocking(False)
                            print("There are new users to chat with!")
                    elif isUsers == "True":
                        print("its true")
                        message = server.recv(1024).decode()
                        print(message)
                else:
                    if isUsers == "True":
                        message = sys.stdin.readline()
                        if (message.strip(' \n\t')).lower() == "exit":
                            isRunning=False
                        else:
                            server.send((f'<{UserName}> : {message}').encode())
                            sys.stdout.write("<You>")
                            sys.stdout.write(message)
                            sys.stdout.flush()
        except:
            continue

    server.close()
