from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import psutil
import sys

class SystemInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setGeometry(320, 480, 320, 480) #Na výšku
        self.setGeometry(480, 320, 480, 320) #Na šířku

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setHtml('''
            <style>
                body {
                    background-image: url("bg.jpg");
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
                    background: #b4b0b0;
                }

                .info-label {
                    font-size: 20px;
                    font-weight: bold;
                }
            </style>
            <body>
            <div class="container">
                <div class="info-row">
                    <div class="info-label">CPU:</div>
                    <div id="cpu"></div>
                    <div class="info-label">HDD:</div>
                    <div id="hdd"></div>
                    <div class="info-label">RAM:</div>
                    <div id="ram"></div>
                    <div class="info-label">GPU:</div>
                    <div id="gpu">N/A</div>
                </div>
            </div>
            </body>
        ''')
        self.browser.loadFinished.connect(self.update_info)
        self.setCentralWidget(self.browser)
        
        #Vytvoří QTimer objekt a spustí jej
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

    def update_info(self):
        cpu = psutil.cpu_percent()
        #hdd = psutil.disk_usage('/').percent
        mem = psutil.virtual_memory().percent
        gpu = "N/A"
        self.browser.page().runJavaScript(f"document.getElementById('cpu').innerHTML = '{cpu}%';")
        #self.browser.page().runJavaScript(f"document.getElementById('hdd').innerHTML = '{hdd}%';")
        self.browser.page().runJavaScript(f"document.getElementById('ram').innerHTML = '{mem}%';")
        self.browser.page().runJavaScript(f"document.getElementById('gpu').innerHTML = '{gpu}';")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SystemInfo()
    window.show()
    sys.exit(app.exec_())
