import sys, requests, csv, traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from qtform1 import Ui_MainWindow
from datetime import datetime,timedelta


app = QtWidgets.QApplication(sys.argv)


MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

def parser(s1,s2,s3):
    try:
        url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID=%s&year1=%s&year2=%s&type=Mean" %(s1,s2,s3)
    
        r = requests.get(url)
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
    soup = BeautifulSoup(r.text, 'html.parser')
    tables=soup.find_all('pre')
    
    namefile='document_'+str(datetime.today().strftime("%H-%M-%S_%d-%m-%Y"))+'.csv'

    with open(namefile,'w') as fd:
        for element in tables:
            row=element.get_text().replace(',  ',',').replace(', ',',')
            fd.write(row)
    readdata(namefile)

            
def readdata(namefile):
    
    data=[]

    frame=pd.read_csv(namefile, delimiter=',', names=['Week','VHI1','VHI2','VHI3','VHI4','VHI5','VHI6'])
    frame.reset_index(level=0, inplace=True)
    frame.columns = ['Year','Week','VHI1','VHI2','VHI3','VHI4','VHI5','VHI6']
    arr=frame[['Year']].to_numpy()

    weeks=-1
    for i in range(len(arr)):
        weeks=weeks+1
        if weeks==52:
            weeks=0
        
        data.append(pd.to_datetime(arr[i]+110000, format='%m%d%Y')+timedelta(days=(7*weeks)))
    frame[['Year']]=data
    bildplot(frame)

    
def bildplot(a):
    
        plt.figure(figsize=(16,9), dpi= 80)
        plt.ylim(0, 100)

        plt.yticks(fontsize=14, alpha=0.7)
        plt.title("VHI (%s - %s)" %(ui.comboBox_2.currentText(),ui.comboBox_4.currentText()), fontsize=22)
        plt.grid(axis='both', alpha=0.25)

        plt.plot(a[['Year']], a[['VHI5']], lw = 2, color = '#539caf', alpha = 1)
        plt.scatter(a['Year'][a[['VHI5']].idxmin()],a[['VHI5']].min(), color='orange',s=40)
        plt.scatter(a['Year'][a[['VHI5']].idxmax()],a[['VHI5']].max(), color='orange',s=40)
        plt.show()

def maindef():
    provinceID=int(ui.comboBox.currentIndex())+1
    year1=ui.comboBox_2.currentText()
    year2=ui.comboBox_4.currentText()
    parser(provinceID,year1,year2)

        
ui.pushButton.clicked.connect(maindef)

sys.exit(app.exec_())
