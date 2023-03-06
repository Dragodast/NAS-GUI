# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QGraphicsDropShadowEffect, QWidget
import RPi.GPIO as GPIO
import subprocess
import psutil
import sys
import time

TACH = 16
PULSE = 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = time.time()
rpm = 0
fan = 'N/A'

class SystemInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setGeometry(320, 480, 320, 480) #Na vysku
        self.setGeometry(480, 320, 480, 320) #Na sirku

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setHtml('''
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap" rel="stylesheet">
            
            <style>
                body {
                    background-image: url("https://cdn.discordapp.com/attachments/670638863127150592/1075695916910133308/bg.jpg");
                    background-size: cover;
                }
            
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                .info-row {
                    display: flex;
                    justify-content: space-between;
                    width: 90%;
                    border-radius: 10px;
                    margin: 10px 0;
                    position: absolute;
                    bottom: 0%;
                    padding: 1%;
                    padding-left: 2%;
                    padding-right: 2%;
                    background: rgba(0, 153, 255, .5);
                    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }

                .info-label {
                    font-size: 20px;
                    font-weight: bold;
                    vertical-align: middle; 
                    font-family: 'Roboto Condensed', sans-serif;
                    color: #c9c9c9;
                }
                
                .info-status {
                    font-size: 20px;
                    vertical-align: middle; 
                    font-family: 'Roboto Condensed', sans-serif;
                    color: #c9c9c9;
                }
                
                .divider {
                  border-left: 2px solid #c9c9c9;
                  height: 23px;
                  vertical-align: middle;
                }

                  /*------*/
                 /* HDDs */
                /*------*/

                .HDD1 {
                    display: grid;
                    width: 90%;
                    border-radius: 10px;
                    margin: 3px 0;
                    position: absolute;
                    bottom: 17%;
                    padding: 2%;
                    background: rgba(0, 153, 255, .5);
                    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }

                .HDD2 {
                    display: grid;
                    width: 90%;
                    border-radius: 10px;
                    margin: 3px 0;
                    position: absolute;
                    bottom: 39%;
                    padding: 2%;
                    background: rgba(0, 153, 255, .5);
                    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }

                .HDD3 {
                    display: grid;
                    width: 90%;
                    border-radius: 10px;
                    margin: 3px 0;
                    position: absolute;
                    bottom: 61%;
                    padding: 2%;
                    background: rgba(0, 153, 255, .5);
                    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }

                .HDD-Texts {
                    display: flex;
                    justify-content: start;
                    margin: 2px 0;
                }

                .divider-hdds {
                  margin-left: 20px;
                  margin-right: 20px;
                  border: 1px solid #c9c9c9;
                  height: 13px;
                  vertical-align: middle;
                }

                .info-hdds {
                    font-size: 14px;
                    font-weight: bold;
                    padding-left: 2px;
                    padding-right: 2px;
                    padding-bottom: 4px;
                    vertical-align: middle; 
                    font-family: 'Roboto Condensed', sans-serif;
                    color: #c9c9c9;
                }

                .HDD-Bar {
                    display: flex;
                    width: 100%;
                    height: 15px;
                    border-radius: 10px;
                    background-color: rgba(102, 102, 102, .8);
                }

                .HDD-Bar-Fill {
                    display: flex;
                    width: 100%;
                    max-width: 100%;
                    height: 15px;
                    border-radius: 10px;
                    background-color: rgb(182, 133, 0);
                }
                
                .HDD-Bar-Fill2 {
                    display: flex;
                    width: 100%;
                    max-width: 100%;
                    height: 15px;
                    border-radius: 10px;
                    background-color: rgb(6, 182, 0);
                }
                
                .HDD-Bar-Fill3 {
                    display: flex;
                    width: 100%;
                    max-width: 100%;
                    height: 15px;
                    border-radius: 10px;
                    background-color: rgb(182, 0, 0);
                }
                
                      /*----------*/
                     /*Start BODY*/
                    /*----------*/
                
            </style>
            
            <body>
            <div class="container">
                <div class="HDD1">
                    <div class="HDD-Texts">
                        <div class="info-hdds">Disk </div>
                        <div class='info-hdds' id="NameHDD1"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Kapacita </div>
                        <div class='info-hdds' id="UsedHDD1"></div>
                        <div class="info-hdds"> / </div>
                        <div class='info-hdds' id="MaxHDD1"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Volné místo </div>
                        <div class='info-hdds' id="FreeHDD1"></div>
                    </div>
                    <div class="HDD-Bar">
                        <div class="HDD-Bar-Fill"></div>
                    </div>
                </div>
                <div class="HDD2">
                    <div class="HDD-Texts">
                        <div class="info-hdds">Disk </div>
                        <div class='info-hdds' id="NameHDD2"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Kapacita </div>
                        <div class='info-hdds' id="UsedHDD2"></div>
                        <div class="info-hdds"> / </div>
                        <div class='info-hdds' id="MaxHDD2"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Volné místo </div>
                        <div class='info-hdds' id="FreeHDD2"></div>
                    </div>
                    <div class="HDD-Bar">
                        <div class="HDD-Bar-Fill2"></div>
                    </div>
                </div>    
                <div class="HDD3">
                    <div class="HDD-Texts">
                        <div class="info-hdds">Disk </div>
                        <div class='info-hdds' id="NameHDD3"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Kapacita </div>
                        <div class='info-hdds' id="UsedHDD3"></div>
                        <div class="info-hdds"> / </div>
                        <div class='info-hdds' id="MaxHDD3"></div>
                        <div class="divider-hdds"></div>
                        <div class="info-hdds">Volné místo </div>
                        <div class='info-hdds' id="FreeHDD3"></div>
                    </div>
                    <div class="HDD-Bar">
                        <div class="HDD-Bar-Fill3"></div>
                    </div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">CPU</div>
                    <div class="info-status" id="cpu"></div>
                    <div class="divider"></div>
                    <div class="info-label">SD</div>
                    <div class="info-status" id="sd"></div>
                    <div class="divider"></div>
                    <div class="info-label">RAM</div>
                    <div class="info-status" id="ram"></div>
                    <div class="divider"></div>
                    <div class="info-label">FAN</div>
                    <div class="info-status" id="fan">N/A</div>
                </div>
            </div>
            </body>
        ''')
        self.browser.loadFinished.connect(self.update_info)
        self.setCentralWidget(self.browser)
        
        #Vytvori QTimer objekt a spustí jej
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.timeout.connect(self.update_disk1)
        self.timer.timeout.connect(self.update_disk2)
        self.timer.timeout.connect(self.update_disk3)
        self.timer.start(1000)
        
        self.fantimer = QtCore.QTimer()
        self.fantimer.timeout.connect(self.update_fan)
        self.fantimer.start(1)
        
        
##########################################################################
## Tlacitka
##########################################################################
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 50).lighter())
        shadow.setOffset(2)
        
        exit_button = QPushButton("X", self)
        exit_button.setGeometry(440, 15, 31, 30)
        exit_button.setGraphicsEffect(shadow)
        exit_button.setStyleSheet("""
                                  
                                background-color: #f44336;
                                border-radius: 10px;
                                font-size: 10px;
                                vertical-align: center; 
                                color: #FFFFFF;
                                font-family: 'Roboto Condensed', sans-serif;
                                font-weight: bold;
                                  
                                  """)
        exit_button.clicked.connect(lambda:self.close())
        
        shutdown_button = QPushButton("Vypnout", self)
        shutdown_button.setGeometry(375, 15, 60, 30)
        shutdown_button.setGraphicsEffect(shadow)
        shutdown_button.setStyleSheet("""
                                  
                                background-color: #f44336;
                                border-radius: 10px;
                                font-size: 10px;
                                vertical-align: center; 
                                color: #FFFFFF;
                                font-family: 'Roboto Condensed', sans-serif;
                                font-weight: bold;
                                  
                                  """)
        shutdown_button.clicked.connect(lambda:self.shutdown())
        
        restart_button = QPushButton("Restartovat", self)
        restart_button.setGeometry(290, 15, 80, 30)
        restart_button.setGraphicsEffect(shadow)
        restart_button.setStyleSheet("""
                                  
                                background-color: #f44336;
                                border-radius: 10px;
                                font-size: 10px;
                                vertical-align: center; 
                                color: #FFFFFF;
                                font-family: 'Roboto Condensed', sans-serif;
                                font-weight: bold;
                                  
                                  """)
        restart_button.clicked.connect(lambda:self.restart())
        
        restart_button = QPushButton("Nastavení", self)
        restart_button.setGeometry(215, 15, 70, 30)
        restart_button.setGraphicsEffect(shadow)
        restart_button.setStyleSheet("""
                                  
                                background-color: #008CBA;
                                border-radius: 10px;
                                font-size: 10px;
                                vertical-align: center; 
                                color: #FFFFFF;
                                font-family: 'Roboto Condensed', sans-serif;
                                font-weight: bold;
                                  
                                  """)
        restart_button.clicked.connect(lambda:self.raspiconfig())
        
        restart_button = QPushButton("Ovládací panel", self)
        restart_button.setGeometry(15, 15, 90, 30)
        restart_button.setGraphicsEffect(shadow)
        restart_button.setStyleSheet("""
                                  
                                background-color: #4CAF50;
                                border-radius: 10px;
                                font-size: 10px;
                                vertical-align: center; 
                                color: #FFFFFF;
                                font-family: 'Roboto Condensed', sans-serif;
                                font-weight: bold;
                                  
                                  """)
        restart_button.clicked.connect(lambda:self.raspiconfig())
        
##########################################################################
## Funkce
##########################################################################
        
    def restart(self):
        subprocess.call(['sudo', 'reboot'])
        
    def shutdown(self):
        subprocess.call(['sudo', 'shutdown', 'now'])
        
    def raspiconfig(self):
        subprocess.call(['sudo', 'raspi-config'])

    def update_info(self):
        cpu = psutil.cpu_percent()
        sd = psutil.disk_usage('/').percent
        mem = psutil.virtual_memory().percent
        
        global fan
        
        self.browser.page().runJavaScript(f"document.getElementById('cpu').innerHTML = '{cpu}%';")
        self.browser.page().runJavaScript(f"document.getElementById('sd').innerHTML = '{sd}%';")
        self.browser.page().runJavaScript(f"document.getElementById('ram').innerHTML = '{mem}%';")
        self.browser.page().runJavaScript(f"document.getElementById('fan').innerHTML = '{fan} RPM';")

            
    def update_fan(self):
        global t
        global rpm
        global fan
        dt = time.time() - t
        if dt < 0.005: return
        
        freq = 1 / dt
        fan = round((freq / PULSE) * 60)
        t = time.time()
                
    def update_disk1(self):
        HDD1Name = '/'
        HDD1Show = 'SD Karta'
        if HDD1Name != 'není':
            HDD1Usage = round(psutil.disk_usage(HDD1Name).used / 1024 / 1024 / 1024)
            HDD1Max = round(psutil.disk_usage(HDD1Name).total / 1024 / 1024 / 1024)
            HDD1Free = round(psutil.disk_usage(HDD1Name).free / 1024 / 1024 / 1024)
            HDD1Percentage = psutil.disk_usage(HDD1Name).percent
            HDD1PercentageCSS = f"{HDD1Percentage}%"
        else:
            HDD1Usage = '0'
            HDD1Max = '0'
            HDD1Free = '0'
            HDD1Percentage = '0'
            HDD1PercentageCSS = f"{HDD1Percentage}%"
            
        self.browser.page().runJavaScript(f"document.getElementsByClassName('HDD-Bar-Fill')[0].style.width = '{HDD1PercentageCSS}';")
        self.browser.page().runJavaScript(f"document.getElementById('NameHDD1').innerHTML = '{HDD1Show}';")
        self.browser.page().runJavaScript(f"document.getElementById('UsedHDD1').innerHTML = '{HDD1Usage}';")
        self.browser.page().runJavaScript(f"document.getElementById('MaxHDD1').innerHTML = '{HDD1Max} GB';")
        self.browser.page().runJavaScript(f"document.getElementById('FreeHDD1').innerHTML = '{HDD1Free} GB';")
        
    def update_disk2(self):
        HDD2Name = "/srv/dev-disk-by-uuid-e27509e5-ef7b-491d-af4a-1bd9e3f60386"
        HDD2Show = 'SSD Kingston'
        if HDD2Name != 'není':
            HDD2Usage = round(psutil.disk_usage(HDD2Name).used / 1024 / 1024 / 1024)
            HDD2Max = round(psutil.disk_usage(HDD2Name).total / 1024 / 1024 / 1024)
            HDD2Free = round(psutil.disk_usage(HDD2Name).free / 1024 / 1024 / 1024)
            HDD2Percentage = psutil.disk_usage(HDD2Name).percent
            HDD2PercentageCSS = f"{HDD2Percentage}%"
        else:
            HDD2Usage = '0'
            HDD2Max = '0'
            HDD2Free = '0'
            HDD2Percentage = '0'
            HDD2PercentageCSS = f"{HDD2Percentage}%"
            
        self.browser.page().runJavaScript(f"document.getElementsByClassName('HDD-Bar-Fill2')[0].style.width = '{HDD2PercentageCSS}';")
        self.browser.page().runJavaScript(f"document.getElementById('NameHDD2').innerHTML = '{HDD2Show}';")
        self.browser.page().runJavaScript(f"document.getElementById('UsedHDD2').innerHTML = '{HDD2Usage}';")
        self.browser.page().runJavaScript(f"document.getElementById('MaxHDD2').innerHTML = '{HDD2Max} GB';")
        self.browser.page().runJavaScript(f"document.getElementById('FreeHDD2').innerHTML = '{HDD2Free} GB';")
    
    def update_disk3(self):
        HDD3Name = 'není'
        HDD3Show = 'není'
        if HDD3Name != 'není':
            HDD3Usage = round(psutil.disk_usage(HDD3Name).used / 1024 / 1024 / 1024)
            HDD3Max = round(psutil.disk_usage(HDD3Name).total / 1024 / 1024 / 1024)
            HDD3Free = round(psutil.disk_usage(HDD3Name).free / 1024 / 1024 / 1024)
            HDD3Percentage = psutil.disk_usage(HDD3Name).percent
            HDD3PercentageCSS = f"{HDD3Percentage}%"
        else:
            HDD3Usage = '0'
            HDD3Max = '0'
            HDD3Free = '0'
            HDD3Percentage = '0'
            HDD3PercentageCSS = f"{HDD3Percentage}%"
        self.browser.page().runJavaScript(f"document.getElementsByClassName('HDD-Bar-Fill3')[0].style.width = '{HDD3PercentageCSS}';")
        self.browser.page().runJavaScript(f"document.getElementById('NameHDD3').innerHTML = '{HDD3Show}';")
        self.browser.page().runJavaScript(f"document.getElementById('UsedHDD3').innerHTML = '{HDD3Usage}';")
        self.browser.page().runJavaScript(f"document.getElementById('MaxHDD3').innerHTML = '{HDD3Max} GB';")
        self.browser.page().runJavaScript(f"document.getElementById('FreeHDD3').innerHTML = '{HDD3Free} GB';")
        
        
############################################################################

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SystemInfo()
    window.show()
    sys.exit(app.exec_())
