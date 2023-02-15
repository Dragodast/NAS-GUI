from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import psutil
import sys
#python -m pip install psutil
#python -m pip install PyQtWebEngine
#python -m pip install PyQt5

class SystemInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(320, 480, 320, 480)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setHtml('''
            <style>
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                .info-row {
                    display: flex;
                    justify-content: space-between;
                    width: 80%;
                    margin: 10px 0;
                }

                .info-label {
                    font-size: 20px;
                    font-weight: bold;
                }
            </style>
            <div class="container">
                <div class="info-row">
                    <div class="info-label">CPU:</div>
                    <div id="cpu"></div>
                </div>
                <div class="info-row">
                    <div class="info-label">HDD:</div>
                    <div id="hdd"></div>
                </div>
                <div class="info-row">
                    <div class="info-label">RAM:</div>
                    <div id="ram"></div>
                </div>
                <div class="info-row">
                    <div class="info-label">GPU:</div>
                    <div id="gpu">N/A</div>
                </div>
            </div>
        ''')
        self.browser.loadFinished.connect(self.update_info)
        self.setCentralWidget(self.browser)

    def update_info(self):
        cpu = psutil.cpu_percent()
        hdd = psutil.disk_usage('/').percent
        mem = psutil.virtual_memory().percent
        gpu = "N/A"
        self.browser.page().runJavaScript(f"document.getElementById('cpu').innerHTML = '{cpu}%';")
        self.browser.page().runJavaScript(f"document.getElementById('hdd').innerHTML = '{hdd}%';")
        self.browser.page().runJavaScript(f"document.getElementById('ram').innerHTML = '{mem}%';")
