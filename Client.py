import socket

# if __name__ == '__main__':

try:
    s = socket.socket()
    host = socket.gethostname()
    print(host)
    port = 12345
    s.connect((host, port))
    while True:
        print("Input from client: ")
        command = input()
        if command == "":
            continue
        elif command == "quit":
            s.send(command)
        elif command == "PrintData":
            s.send(command.encode())
            data = s.recv(1024)
            print(data)
        elif command == "EditCity":
            s.send(command.encode())
            print("enter id")
            id = int(input())
            s.send(str(id).encode())
            print("Choose what to change")
            comm = int(input())
            s.send(str(comm).encode())
            data = s.recv(1024)
            print(data)
            print("Value ")
            val = input()
            s.send(val.encode())
            result = s.recv(1024)
        elif command == "Cities":
            s.send(command.encode())
            print("Enter id of a country")
            id = int(input())
            s.send(str(id).encode())
            data = s.recv(1024)
            print(data)
        elif command == "EditCountry":
            s.send(command.encode())
            print(" EDIT COUNTRY")
            id = int(input())
            s.send(str(id).encode())
            com = int(input())
            s.send(str(com).encode())
            print("Enter new name")
            name = input()
            s.send(name.encode())
        elif command == "DeleteCity":
            s.send(command.encode())
            print("delete city")
            print("Enter id of a city")
            id = int(input())
            s.send(str(id).encode())
        elif command == "AddCountry":
            s.send(command.encode())
            print("Enter the id of a country")
            id = int(input())
            s.send(str(id).encode())
            name = input()
            s.send(name.encode())

            #print(result)
        #print(data)
        #print(command)
except:
    print("Disconnected from server")
# s = socket.socket()
# host = socket.gethostname()
# print(host)
# port = 12345
# s.connect((host, port))
# s.send(b'hello, world!')
#
# data = s.recv(1024)
# s.close()
#
# print(data)
# while True:
#     command = input()
#     if command == "":
#         continue
#     elif command == "quit":
#         s.send(command.encode())
#     print(command)