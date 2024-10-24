from PyQt5.QtWidgets import QApplication
from pyqtwindow import QtWindow,WindowManager
import threading
import sys
from time import sleep

def main(argv:list):
    # Colors of different Gui Elements can be set here globally
    # Alternatively they will be shown in their default colors
    QtWindow.backgroundcolor = "#c1e1ec;"
    QtWindow.button_color = "#68BBE3"
    QtWindow.abort_button_color = "#FF5C5C"
    QtWindow.defaultButton_color = "#AAFF00"
    # Window can have a close and a maximize button but doesn't need to
    # Default is False for both cases
    QtWindow.closeButton = True
    QtWindow.maximizeButton = False
    ##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    # starts the actualt application
    app = QApplication(argv)
    # creation of Gui Windows
    # Here you can set if an how many buttons, images, input fields, ... a window should have
    # Also it is possible to a a title and further text content or to set a default button
    # check out the README for more detailed informations
    window1 = QtWindow("Window 1","This is the first window.\nClick on 'Next' to continue.",button_count=1,buttons_textlabels=["Next"],abort_button=False)
    window2 = QtWindow("Window 2","Click 'Count to 10' to start two successive threads. Afterwards the new window will automatically.\nAlternatively click 'Next' to continue without executing the threads or 'Abort' to terminate the program",button_count=3,buttons_textlabels=["Count to 10","Next","Abort"])
    window3 = QtWindow("Window 3","Check out this beautiful image.\nAfterwards click 'Next' to continue or press Enter to click the default button 'Next Default'",button_count=3,buttons_textlabels=["Next","Next Default","Abort"],image_count=1,image_paths=["./alley.jpg"],defaultButton="Next Default")
    window4 = QtWindow("Window 4","As you can see each image has its own button now.\nClick on any button to start a thread which will count up.\nAfterwards the next window will be opened automatically.",button_count=5,buttons_per_row=2,buttons_textlabels=["Count to 5","Count to 10","Count to 15","Count to 20","Abort"],image_count=4,image_paths=["alley.jpg","alley.jpg","alley.jpg","alley.jpg"],img_button_connect=True,defaultButton="Count to 10")
    window5 = QtWindow("Window 5","Click 'Open Popup' to open a popup window.\nAfter closing the popup window click 'Next' to continue.",button_count=3,buttons_textlabels=["Open Popup","Next","Abort"],defaultButton="Open Popup")
    popupWindow = QtWindow("Popup Window","This is some important Message",button_count=1,buttons_textlabels=["Close"],abort_button=False,defaultButton="Close")
    window6 = QtWindow("Window 6","Type something in the Input Field and click 'Next' to output it to the terminal while opening the next window",button_count=2,buttons_textlabels=["Print Text","Abort"],input_field=True,nbr_of_input_fields=1)
    window7 = QtWindow("Window 7", "If you click 'Select File' your file explorer will open and you will be able to select a file.\nThis is the last window of the little demo",button_count=2,buttons_textlabels=["Select File","Abort"],defaultButton="Select File")
    
    # Open the first window of the routine
    WindowManager.openNewWindow(None,window1)
    ##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    # in the following section the flow of the actual program is implemented
    # button clicks are connected with according functions etc.
    window1.buttons["Next"].clicked.connect(lambda: WindowManager.openNewWindow(window1,window2))

    window2.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    countTo10 = threading.Thread(target=countToX,args=(10,),daemon=True)
    printHey = threading.Thread(target=printSth,args=("Hey",),daemon=True)
    run_ths = threading.Thread(target=run_threads,args=([countTo10,printHey],window2),daemon=True)
    window2.buttons["Count to 10"].clicked.connect(lambda: run_ths.start())
    window2.buttons["Next"].clicked.connect(lambda: WindowManager.openNewWindow(window2,window3))
    window2.finished.connect(lambda: WindowManager.openNewWindow(window2,window3))

    window3.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    window3.buttons["Next Default"].clicked.connect(lambda: WindowManager.openNewWindow(window3,window4))
    window3.buttons["Next"].clicked.connect(lambda: WindowManager.openNewWindow(window3,window4))

    window4.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    countTo5 = threading.Thread(target=countToX,args=(5,),daemon=True)
    countTo10 = threading.Thread(target=countToX,args=(10,),daemon=True)
    countTo15 = threading.Thread(target=countToX,args=(15,),daemon=True)
    countTo20 = threading.Thread(target=countToX,args=(20,),daemon=True)
    run_countTo5 = threading.Thread(target=run_threads,args=([countTo5],window4),daemon=True)
    run_countTo10 = threading.Thread(target=run_threads,args=([countTo10],window4),daemon=True)
    run_countTo15 = threading.Thread(target=run_threads,args=([countTo15],window4),daemon=True)
    run_countTo20 = threading.Thread(target=run_threads,args=([countTo20],window4),daemon=True)
    window4.buttons["Count to 5"].clicked.connect(lambda: run_countTo5.start())
    window4.buttons["Count to 10"].clicked.connect(lambda: run_countTo10.start())
    window4.buttons["Count to 15"].clicked.connect(lambda: run_countTo15.start())
    window4.buttons["Count to 20"].clicked.connect(lambda: run_countTo20.start())
    window4.finished.connect(lambda: WindowManager.openNewWindow(window4,window5))

    window5.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    goOn = threading.Event()
    popupWindow.buttons["Close"].clicked.connect(lambda: goOn.set())
    popupWindow.open_.connect(lambda: popupWindow.show())
    popupWindow.close_.connect(lambda: popupWindow.hide())
    openPopupWindow = threading.Thread(target=openPopup,args=(popupWindow,goOn),daemon=True)
    runOpenPopup = threading.Thread(target=run_threads,args=([openPopupWindow],window5,False),daemon=True)
    window5.buttons["Open Popup"].clicked.connect(lambda: runOpenPopup.start())
    window5.buttons["Next"].clicked.connect(lambda: WindowManager.openNewWindow(window5,window6))

    window6.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    printInput = threading.Thread(target=printInputText,args=(window6,),daemon=True)
    do_printInput = threading.Thread(target=run_threads,args=([printInput],window6),daemon=True)
    window6.buttons["Print Text"].clicked.connect(lambda: do_printInput.start())
    window6.finished.connect(lambda: WindowManager.openNewWindow(window6,window7))

    window7.buttons["Abort"].clicked.connect(lambda: WindowManager.closeAll(app))
    window7.buttons["Select File"].clicked.connect(lambda: window7.get_file(window7,"./","Text files (*.txt)"))
    window7.close_.connect(lambda: WindowManager.closeAll(app))
    
    # pass exit code after termination of event-loop to sys.exit()
    # good practice but not strictly necessary
    sys.exit(app.exec())

    ##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# Functions connected with button clicks
# counts up to x
def countToX(x:int):
    for i in range(1,x+1):
        print(i)
        sleep(0.5)

# prints any string s
def printSth(s:str):
    print(f"Important message: {s}")

# opens a popup window and waits until an Event is set to continue
def openPopup(popupWindow:QtWindow,continueEvent:threading.Event):
    # Signal used to show popup window
    popupWindow.open_.emit()
    # waiting until Event is set
    # usually the Event is set when the user clicks a button of the popup window
    while not continueEvent.is_set():
        sleep(0.5)
    continueEvent.clear()
    # Signal used to close popup window
    popupWindow.close_.emit()

# output text of input field
def printInputText(window:QtWindow):
    print(window.inputs[0].text())

# runs and joins threads successively
# optional: sending signal that finished back to the gui window
def run_threads(threads:list[threading.Thread],window:QtWindow,sendFinish:bool=True):
    for thread in threads:
        thread.start()
        thread.join()
    if sendFinish:
        window.finished.emit()

    

if __name__ == "__main__":
    main(sys.argv)

# alley.jpg von PublicDomainPictures (https://pixabay.com/de/photos/gasse-stra%C3%9Fe-nacht-abend-stadt-89197/)