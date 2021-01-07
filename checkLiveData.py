import sys
import threading

from PyQt5 import QtCore, QtWidgets, uic
import mysql.connector
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import requests
import os
import sys
import re
import json


mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test", autocommit=True)
cursor = mydb.cursor()



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("CheckLiveData.ui", self)
        self.UpdataData.released.connect(lambda: newCases())
        
        def newCases():
            
            locality = self.lineEdit.text().title()
            self.lineEdit.clear()         
            print(locality)
            #global population
            
            try:
                #print(population)
                search(locality)
                #print(Grecovered)
                try:
                    conpop = str(round((Gconfirmed/population) * 100, 2))
                    actpop = str(round((Gactive/population) * 100, 2))
                    recpop = str(round((Grecovered/population) * 100, 2))
                    detpop = str(round((Gdeaths/population) * 100, 2))


                    self.conper.setText(conpop + "%")
                    self.actper.setText(actpop + "%")
                    self.recper.setText(recpop + "%")
                    self.detper.setText(detpop + "%")
                except:
                    pass
                
                
                self.UpdataData_2.setText(locality + " Current" + " Status")
                self.Confirmed.setText("Confirmed\n{:,}".format(Gconfirmed))
                self.Active.setText("Active\n{:,}".format(Gactive))
                self.Recovered.setText("Recovered\n{:,}".format(Grecovered))
                self.Deaths.setText("Deaths\n{:,}".format(Gdeaths))
                print(type(Gdeaths))
                self.Title_3.setText("")
                self.lineEdit.clear()


            except (ValueError):
                countrySearch(locality)
                if type(Cconfirmed) == int:



                    self.UpdataData_2.setText(locality + " Current" + " Status")
                    self.Confirmed.setText("Confirmed\n{:,}".format(int(Cconfirmed)))
                    self.Active.setText("Active\n{:,}".format(int(Cactive)))
                    self.Recovered.setText("Recovered\n{:,}".format(int(Crecovered)))
                    self.Deaths.setText("Deaths\n{:,}".format(int(Cdeaths)))
                    self.Title_3.setText("")
                    self.lineEdit.clear()

                    self.conper.setText("")
                    self.actper.setText("")
                    self.recper.setText("")
                    self.detper.setText("")

                    

                else:
                    print("in")

                    self.conper.setText("")
                    self.actper.setText("")
                    self.recper.setText("")
                    self.detper.setText("")

                    self.Title_3.setText("Invalid")
                    self.UpdataData_2.setText("")
                    self.Confirmed.setText("Confirmed\n - - -")
                    self.Active.setText("Active\n - - -")
                    self.Recovered.setText("Recovered\n - - -")
                    self.Deaths.setText("Deaths\n - - -")


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Ui()
    window.show()

    app.exec_()


def net_check():
    try:
        requests.get("https://www.google.com/")
        return True
    except:
        print("Net fail")
        return False


def search(locality):
    global Gconfirmed
    global Gactive
    global Grecovered
    global Gdeaths

    if locality == "India":
        #print("India")
        cursor.execute("SELECT SUM(confirmed) FROM dis")
        Gconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("SELECT SUM(active) FROM dis")
        Gactive = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("SELECT SUM(recovered) FROM dis")
        Grecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("SELECT SUM(deaths) FROM dis")
        Gdeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        return None

    try:
        global population
        cursor.execute("select population from populati where districts = %s", (locality,))
        population = int(re.sub("[,()'']", "", str(cursor.fetchone())))

        

        cursor.execute("select confirmed from dis where districts = %s", (locality,))
        Gconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
 
        cursor.execute("select active from dis where districts = %s", (locality,))
        Gactive = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select recovered from dis where districts = %s", (locality,))
        Grecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select deaths from dis where districts = %s", (locality,))
        Gdeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))


    except (ValueError):
        
        
        cursor.execute("select confirmed from state where states = %s", (locality,))
        Gconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select active from state where states = %s", (locality,))
        Gactive  = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select recovered from state where states = %s", (locality,))
        Grecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select deaths from state where states = %s", (locality,))
        Gdeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
 
def countrySearch(locality):

    global Cconfirmed
    global Cactive
    global Crecovered
    global Cdeaths

    try:
        country = locality.lower().replace(" ", "-")
        url = f'https://www.worldometers.info/coronavirus/country/{country}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        data = []

        for x in range(0, 3):
            x = soup.find_all(class_ = 'maincounter-number')[x].find('span').text
            data.append(x)

        Active = int((re.sub("[],]","", data[0]))) - (int((re.sub("[],]","", data[1]))) + int((re.sub("[],]","", data[2]))))

        res = "{:,}".format(Active)
        print("\n" + country.title())
        print ("\nTotal cases:" + data[0])
        print ("Deaths:" + data[1])
        print ("Recovered:" + data[2])
        print("Active Cases:" + str(res)+   "\n")

        Cconfirmed = int((re.sub("[],]","", data[0])))
        Cactive = Active
        Crecovered = int((re.sub("[],]","", data[2])))
        Cdeaths = int((re.sub("[],]","", data[1])))

    except:
        print("fail")
        Cconfirmed = ""
        Cactive = ""
        Cdeaths = ""
        Crecovered = ""


def population():
    population_url = 'https://api.covid19india.org/misc.json'
    r = urllib.request.urlopen(population_url) 

    data = r.read().decode() 
    js = json.loads(data)
    population_list = []
    district_list = []

    population_list = [i['population'] for i in js['district_meta_data']]
    #print(population_list)
    district_list = [i['district'] for i in js['district_meta_data']]
    #print(type(district_list))

    cursor.execute("DROP TABLE populati")
    cursor.execute("CREATE TABLE populati(districts LONGTEXT, population LONGTEXT)")
    query = "INSERT INTO populati (districts, population) values (%s, %s)"
    cursor.executemany(query, [(a) for a in zip(district_list, population_list)])
   


if __name__ == "__main__":
    main()
    #population()
