import sqlite3
from pathlib import Path


class WorldMap:
    _cur = None
    _conn = None

    def __init__(self):
        self._curFile = ""

    def setCurFile(self, file):
        self._curFile = file

    def create(self, file, networkConn):
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        print(cur)
        print(conn)
        print("Opened database successfully")
        my_file = Path(file)
        if my_file.is_file():
            message = "ERROR" + '#' + "file already exists"
            # file exists
            # if os.path.isfile(file):
            networkConn.send(message.encode())
            print("File exists")
            return
        conn.execute('''
        CREATE TABLE IF NOT EXISTS country_data(id_co integer, 
                          name text);''')

        cur.execute('''CREATE TABLE \"Country\" (
    			\"ID\"	INTEGER NOT NULL UNIQUE,
    			\"NAME\"	TEXT,
    			PRIMARY KEY(\"ID\")
    		)''')
        cur.execute('''CREATE TABLE \"City\" (
    			\"ID_CI\"	INTEGER NOT NULL UNIQUE,
    			\"NAME\"	INTEGER,
    			\"ISCAP\"	SMALLINT,
    			\"COUNT\"	INTEGER,
    			\"COUNTRY_ID\"	INTEGER,
    			PRIMARY KEY(\"ID_CI\")
    		)''')
        print("Table created successfully")
        conn.commit()
        conn.close()
        self.connect(file)

    def connect(self, file):
        self.setCurFile(file)
        self._conn = sqlite3.connect(file)
        self._cur = self._conn.cursor()
        print(self._cur)
        print(self._conn)

    def addCountry(self, id, name):
        self.connect("dataBase.db")
        # print("Enter id of a new country: ")
        #
        # print("Enter the name of a new country: ")

        self._cur = self._conn.cursor()
        print(self._cur)
        print(self._conn)
        self._conn.execute("INSERT INTO Country VALUES(%d, '%s')" % (id, name))
        self._conn.commit()

    def PrintData(self, networkConn):
        self.connect("dataBase.db")
        sql = "SELECT ID, NAME FROM Country"
        self._cur.execute(sql)
        results = self._cur.fetchall()
        output = ""
        for row in results:
            idCountry = row[0]
            nameCountry = row[1]
            print("Country id: " + str(idCountry) + ", name: " + nameCountry)
            output = output + "Country id: " + str(idCountry) + ", name: " + nameCountry + " \n "
        sql = "SELECT ID_CI, NAME, ISCAP, COUNT, COUNTRY_ID FROM City"
        self._cur.execute(sql)
        results = self._cur.fetchall()

        for row in results:
            idCity = row[0]
            cityName = row[1]
            cityIscap = row[2]
            cityCount = row[3]
            countryId = row[4]
            print("City id: " + str(idCity) + ", name: " + cityName + ", Is capital: " + str(
                cityIscap) + " City Count: " + str(cityCount) + " Country ID: " + str(countryId))
            output = output + "City id: " + str(idCity) + ", name: " + cityName + ", Is capital: " + str(
                cityIscap) + " City Count: " + str(cityCount) + " Country ID: " + str(countryId) + " \n "
        message = "Text" + "#" + output
        networkConn.send(message.encode())
        return message
    def deleteCountry(self):
        print("Enter id of a country to delete it: ")
        id = int(input())
        statement = "DELETE FROM Country WHERE ID = " + str(id)
        self._cur.execute(statement)
        statement = "DELETE FROM City WHERE COUNTRY_ID = " + str(id)
        self._cur.execute(statement)
        self._conn.commit()

    def addCity(self):
        print("Enter the id of a new city: ")
        id = int(input())
        print("Enter the name of a new city: ")
        name = input()
        print("Enter iscap: ")
        iscap = int(input())
        print("Enter count: ")
        count = int(input())
        print("Enter country ID: ")
        countryId = int(input())

        self._cur = self._conn.cursor()
        # print(self._cur)
        # print(self._conn)
        self._conn.execute("INSERT INTO City VALUES(%d, '%s', %d, %d, %d)" % (id, name, iscap, count, countryId))
        self._conn.commit()

    def deleteCity(self, id, conn):
        self.connect("dataBase.db")
        print("Delete city with id: ")

        sql = "DELETE FROM City WHERE ID_CI = " + str(id)
        self._cur.execute(sql)
        self._conn.commit()
        #####################################

    def editCity(self,id, conn, com):
        self.connect("dataBase.db")
        print("Command for editing city: with id: ", id)
        print("choose what to edit: ")
        # com = int(input())
        #conn.send()

        sqlCommand = "Update City SET "

        if com == 1:
            print("Enter new name(String)")
            message = "Enter new name(String)"
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            print(data)
            sqlCommand = sqlCommand + "NAME = '" + str(data) + "'"
            print(sqlCommand)
        elif com == 2:
            print("Enter new iscap(int)")
            data = conn.recv(1024).decode()
            sqlCommand = sqlCommand + "ISCAP = '" + str(data) + "'"
        elif com == 3:
            print("Enter new count(int)")
            data = conn.recv(1024).decode()
            sqlCommand = sqlCommand + "COUNT = '" + str(data) + "'"
        elif com == 4:
            print("Enter new city ID(int)")
            data = conn.recv(1024).decode()
            sqlCommand = sqlCommand + "ID_CI = '" + str(data) + "'"
        elif com == 5:
            print("Enter new country ID(int)")
            data = conn.recv(1024).decode()
            sqlCommand = sqlCommand + "COUNTRY_ID = '" + str(data) + "'"
        sqlCommand = sqlCommand + " WHERE ID_CI = " + str(id)
        print(sqlCommand)
        self._cur.execute(sqlCommand)
        self._conn.commit()


    def undo(self):
        self._conn.rollback()
        print("data rolled back")
        # sql = sql + "nameProduct = '" + productName + "'"
        ######################

    def editCountry(self, id,comm,conn):
        self.connect("dataBase.db")

        sqlCommand = "UPDATE Country SET "
        if comm == 1:
            print("Enter new name(string)")
            data = conn.recv(1024).decode()
            sqlCommand = sqlCommand + "NAME = '" + str(data) + "'"
        sqlCommand = sqlCommand + " WHERE ID = " + str(id)
        print(sqlCommand)
        self._cur.execute(sqlCommand)
        self._conn.commit()
        ###############################

    def getCountryById(self, id):
        sql = "SELECT * FROM Country WHERE ID = %d" % id
        self._cur.execute(sql)
        result = self._cur.fetchall()
        for x in result:
            print(x)

    def printCities(self, id, networkConn):
        self.connect("dataBase.db")
        # sql = "SELECT \
        # Country.NAME AS country, \
        # City.NAME AS city \
        # FROM city \
        # INNER JOIN country ON city.COUNTRY_ID = country.ID"
        # sql = "SELECT \
        # Country.NAME AS country, \
        # City.NAME AS city \
        # FROM country \
        # INNER JOIN city ON %d = city.COUNTRY_ID" % id
        sql = "SELECT * FROM City WHERE COUNTRY_ID = %d" % id
        self._cur.execute(sql)
        output = ""
        myresult = self._cur.fetchall()
        for x in myresult:
            print(x)
            output = output + str(x)
        message = "Text" + "#" + output
        #networkConn.send(message.encode())
        return message

    def commandProcessor(self, command, netConn):
        if command == "PrintData":
            self.PrintData(netConn)
            netConn.send()
        elif command == "printCities":
            print("ID OF THE COUNTRY: ")
            countryId = int(input())
            self.printCities(countryId, netConn)
