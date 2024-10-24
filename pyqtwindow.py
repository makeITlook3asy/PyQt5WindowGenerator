from PyQt5.QtWidgets import QMainWindow,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QWidget,QApplication,QLineEdit,QFileDialog,QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal

class QtWindow(QMainWindow):
    # signal used to communicate between threads and gui windows
    close_ = pyqtSignal()
    open_ = pyqtSignal()
    finished = pyqtSignal()
    # default color of different gui elements
    backgroundcolor = "#c1e1ec;"
    button_color = "#68BBE3"
    abort_button_color = "#FF5C5C"
    defaultButton_color = "#AAFF00"
    # per default there is neither a close nor a maximize button
    closeButton = False
    maximizeButton = False
    
    # Constructur of class which creates a gui window with specific properties
    def __init__(self,title:str,text:str,button_count:int = 0,buttons_textlabels:list = list(),image_count:int = 0,
                 image_paths:list = list(), abort_button:bool = True, text_centered:bool = True, input_field = False,nbr_of_input_fields:int = 1, buttons_per_row = 4,
                stays_on_top:bool = False,img_button_connect:bool = False,disableButton:bool = True,defaultButton:str = ""):
        QMainWindow.__init__(self)
        # text content of window
        self.text = text
        # amount of buttons
        self.button_count = button_count
        # text of buttons
        self.buttons_textlabels = buttons_textlabels
        # is there a abort button
        self.abort_button = abort_button
        # amount of images
        self.image_count = image_count
        # where can the images be found?
        self.image_paths = image_paths
        # should the text be centered?
        self.text_centered = text_centered
        # should the window have an input field
        self.input_field = input_field
        # amount of input fields
        self.nbr_of_input_fields = nbr_of_input_fields
        # max number of buttons per row
        self.buttons_per_row = buttons_per_row
        # disabling buttons after click?
        self.disableButton = disableButton
        # default button and if yes which one?
        self.defaultButton = defaultButton
        # arrangement of buttons and images: do they belong together or not
        self.img_button_connect = img_button_connect
        # center window
        self.center()
        # enabling or disabling close and maximize button
        self.setWindowFlag(Qt.WindowCloseButtonHint, self.closeButton)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, self.maximizeButton)
        # window opens on top of all other windows if this Flag is set
        if stays_on_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint,True)
        # creates alls Components
        self.createComponents()
        # combines components in a layout
        self.createLayout()
        # set title of window
        self.setWindowTitle(title)
        # set background color of window
        self.setStyleSheet(f'background-color: {QtWindow.backgroundcolor}')

    # opens a window
    def show(self) -> None:
        # set default button if present
        if self.defaultButton != "":
            defBut = self.defaultButton
            self.buttons[defBut].setDefault(True)
            self.buttons[defBut].setFocus()
            self.buttons[defBut].setStyleSheet(f"background-color: {QtWindow.defaultButton_color}")
        # open window
        super().show()

    # center window on screen
    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
    
    # create different gui elements
    def createComponents(self) -> None:
        # set text content
        self.textlabel = QLabel(self.text)
        if self.text_centered == True:
            self.textlabel.setAlignment(Qt.AlignCenter)

        # create buttons with the correct color and text
        self.buttons = dict()
        button_color = QtWindow.button_color
        for i in range(self.button_count):
            if i == self.button_count - 1 and self.abort_button == True:
                button_color = QtWindow.abort_button_color
            self.buttons[self.buttons_textlabels[i]]=(self.createButton(self.buttons_textlabels[i],button_color,self.disableButton))

        # create images
        self.images = list()
        for i in range(self.image_count):
            pixmap = self.createPixmap(self.image_paths[i])
            img_label = self.createImageLabel(pixmap)
            img_label.setPixmap(pixmap)
            self.images.append(img_label)

        # create input filed
        if self.input_field:
            self.input_lay = QHBoxLayout()
            self.inputs = list()
            for i in range(self.nbr_of_input_fields):
                self.inputs.append(QLineEdit(self))
                self.input_lay.addWidget(self.inputs[i])

    # combine different gui elements in a layout
    def createLayout(self):
        # main layout is a vertical one: so we use QVBoxLayout
        layoutCentral = QVBoxLayout()
        # add text content to layout
        layoutCentral.addWidget(self.textlabel)
        # add images to layout if they don't belong to a specific button
        if self.image_count > 0 and not self.img_button_connect:
            # images are shwon in a horizontal layout
            image_layout = QHBoxLayout()
            for image in self.images:
                image_layout.addWidget(image)
            image_layout.setAlignment(Qt.AlignHCenter)
            # add horizontal image layout to vertical main layout
            layoutCentral.addLayout(image_layout)
        # add input filed to layout
        if self.input_field:
            layoutCentral.addLayout(self.input_lay)
        # add buttons to layout in dependence of the max number of buttons per row
        if self.button_count > 0 and self.button_count <= self.buttons_per_row:
            # if images and buttons belong together we need to add a horizontal image layout first here
            if self.img_button_connect:
                image_layout = QHBoxLayout()
                for image in self.images:
                    image_layout.addWidget(image)
                layoutCentral.addLayout(image_layout)
            # create horizontal layout for buttons
            button_layout = QHBoxLayout()
            for name,button in self.buttons.items():
                button_layout.addWidget(button)
            # add horizontal button layout to vertical main layout
            layoutCentral.addLayout(button_layout)

        # if the number of buttons is bigger than max amount of buttons per row 
        # we need more than one line of buttons (and images if necessary)
        if self.button_count > self.buttons_per_row:
            button_layout_1 = QHBoxLayout()
            button_layout_2 = QHBoxLayout()
            button_layout_3 = QHBoxLayout()
            button_layout_4 = QHBoxLayout()
            button_layout_5 = QHBoxLayout()
            if self.img_button_connect:
                image_layout_1 = QHBoxLayout()
                image_layout_2 = QHBoxLayout()
                image_layout_3 = QHBoxLayout()
                image_layout_4 = QHBoxLayout()
                image_layout_5 = QHBoxLayout()
            counter = 0
            for name,button in self.buttons.items():
                if counter < self.buttons_per_row:
                    button_layout_1.addWidget(button)
                    if self.img_button_connect:
                        if name != "Abort" and name != "":
                            image_layout_1.addWidget(self.images[counter])
                        else:
                            image_layout_1.addWidget(QWidget())
                            
                    counter += 1
                elif self.buttons_per_row <= counter and counter < 2 * self.buttons_per_row:
                    button_layout_2.addWidget(button)
                    if self.img_button_connect:
                        if name != "Abort" and name != "":
                            image_layout_2.addWidget(self.images[counter])
                        else:
                            image_layout_2.addWidget(QWidget())
                            
                    counter += 1
                elif 2 * self.buttons_per_row <= counter < 3 * self.buttons_per_row:
                    button_layout_3.addWidget(button)
                    if self.img_button_connect:
                        if name != "Abort" and name != "":
                            image_layout_3.addWidget(self.images[counter])
                        else:
                            image_layout_3.addWidget(QWidget())
                            
                    counter += 1
                elif 3 * self.buttons_per_row <= counter < 4 * self.buttons_per_row:
                    button_layout_4.addWidget(button)
                    if self.img_button_connect:
                        if name != "Abort" and name != "":
                            image_layout_4.addWidget(self.images[counter])
                        else:
                            image_layout_4.addWidget(QWidget())

                    counter += 1
                else:
                    button_layout_5.addWidget(button)
                    if self.img_button_connect:
                        if name != "Abort" and name != "":
                            image_layout_5.addWidget(self.images[counter])
                        else:
                            image_layout_5.addWidget(QWidget())
                            
            if self.img_button_connect:
                layoutCentral.addLayout(image_layout_1)
            layoutCentral.addLayout(button_layout_1)
            if self.img_button_connect:
                layoutCentral.addLayout(image_layout_2)
            layoutCentral.addLayout(button_layout_2)
            if self.img_button_connect:
                layoutCentral.addLayout(image_layout_3)
            layoutCentral.addLayout(button_layout_3)
            if self.img_button_connect:
                layoutCentral.addLayout(image_layout_4)
            layoutCentral.addLayout(button_layout_4)
            if self.img_button_connect:
                layoutCentral.addLayout(image_layout_5)
            layoutCentral.addLayout(button_layout_5)

        # finally set the main layout as the window's central image
        widgetCentral = QWidget()
        widgetCentral.setLayout(layoutCentral)
        self.setCentralWidget(widgetCentral)

    # create a button with text, background color , possibility to be disabled after click 
    # which prints 'user clicked button name' when clicked
    def createButton(self, text : str, color: str, disableButton:bool = True) -> QPushButton:
        # create button with text
        button = QPushButton(text)
        # set auto default (if False setting Default button isn't possible)
        button.setAutoDefault(True)
        # backgroundcolor
        button.setStyleSheet(f"background-color: {color}")
        # disable button after click (usefull to prevent threads from being started twice)
        if disableButton:
            button.clicked.connect(lambda: button.setEnabled(False))
        # prints which button was clicked by user to terminal output
        button.clicked.connect(lambda: print(f"User clicked '{text}'"))
        return button
    
    def createPixmap(self,image_path : str) -> QPixmap:
            pixmap = QPixmap(image_path)
            return pixmap
    
    def createImageLabel(self,pixmap : QPixmap) -> QLabel:
        label = QLabel()
        label.setPixmap(pixmap)
        return label
    
    # select file from file system at path_to_folder location an filter specific file type
    def get_file(self,current_window,path_to_folder:str,filter:str):
        # open file system window 
        self.dialog = QFileDialog(self)
        # get name of file user selected
        fname = self.dialog.getOpenFileName(self,'Select file',path_to_folder,filter)
        print(f"{fname[0]} selected")
        # send Signal to close current window
        current_window.close_.emit()
        

class WindowManager():
    # open new gui window and close old one
    @staticmethod
    def openNewWindow(currentWindow: QtWindow,newWindow: QtWindow):
        try:
            if currentWindow is None:
                newWindow.show()
                newWindow.center()
            else:
                for name, button in currentWindow.buttons.items():
                    button.setEnabled(True)
                currentWindow.window = newWindow
                currentWindow.window.show()
                currentWindow.window.center()
                currentWindow.hide()
        except Exception as e:
            raise(e)

    # enable a disabled button again
    @staticmethod    
    def enable_buttons(window):
        for name, button in window.buttons.items():
            button.setEnabled(True)
    
    # close all currently opened gui windows
    @staticmethod
    def closeAll(app:QApplication):
        app.closeAllWindows()


