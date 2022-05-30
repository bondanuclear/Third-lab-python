import socket
import DataBaseController as dbController
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    print(host)
    #s.listen(5)
   # print('Waiting for a client')
    #conn, addr = s.accept()
   # print('Got connection from ', addr)
    try:
        while True:
            s.listen()
            print('Waiting for a client')
            conn, addr = s.accept()
            print('Got connection from ', addr)
            manager = dbController.WorldMap()

            while True:
                command = conn.recv(1024).decode()
                print("Command at server.py", command)
                if command == "quit":
                    exit()
                #manager.commandProcessor(command, conn)
                elif command == "PrintData":
                    message = manager.PrintData(conn)
                    print(message, "MESSAGE")
                    conn.send(message.encode())
                elif command == "EditCity":
                    message = "Enter following "
                    id = conn.recv(1024).decode()
                    print(id + "ID SERVER")
                    com = conn.recv(1024).decode()
                    print(com + "COMMAND")
                    manager.editCity(int(id), conn, int(com))
                    message = manager.PrintData(conn)
                    conn.send(message.encode())
                elif command == "Cities":
                    id = conn.recv(1024).decode()
                    print(id + " CITIES ")
                    message = manager.printCities(int(id), conn)
                    #message = conn.recv(1024).decode()
                    print(message + " CITIES")
                    conn.send(message.encode())
                elif command == "EditCountry":
                    id = conn.recv(1024).decode()
                    print(id + " ID EDIT COUNTRY")
                    com = conn.recv(1024).decode()
                    print("COmmand " + com)
                    manager.editCountry(int(id), int(com), conn)
                elif command == "DeleteCity":
                    id = conn.recv(1024).decode()
                    print(id + " ID Delete city")
                    manager.deleteCity(int(id), conn)
                elif command == "AddCountry":
                    id = conn.recv(1024).decode()
                    print("id of a new country" + id)
                    name = conn.recv(1024).decode()
                    print("name of a new country " + name )
                    manager.addCountry(int(id), name)

    except KeyboardInterrupt:
        print("Server stopped")