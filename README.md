# PyQt5 Window Generator
***
## General overview
The PyQt5 Window Generator can be used to create and customize PyQt gui windows as well as to implement a coherent program flow out of these windows. 
It is possible to customize the following aspects of a gui window:
* colors of it elements (buttons,background...)
* presence of a maximize or close button
* content of the title 
* text content 
* amount, text and arrangement of buttons
* amount of images
* ensemble of buttons and images
* amount of input fields and handling of user input
* existence of an abort button
* setting of a default button
* disabling buttons after click or not
***
## Installation
First of all a version of **Python 3** has to be installed on your system. 
Right now I am using Python 3.10.12.
Furthermore you have to install **PyQt5** which can be done by via Pip using the following command: `pip install PyQt5`.
Apart from that the following Python moduls are used:
* sys
* threading
* time

Afterwards you can download both Python files and run them by using the `python3 example.py` or `python example.py` command (depending on your system variables).
***
## pyqtwindow<area>.py 
Contains the following two classes: **QtWindow** which is used to create customized gui windows and **WindowManager** which is used to handle the opening and closing process of windows as well as the enabling of disabled buttons.
### 1) QtWindow
#### 1.1 Class Attributes
* close_ : Signal that can be send to signalize that a window should be closed
* open_ : Signal that can be send to signalize that a window should be opened
* finished : Signal that can be send to signalize that a functions has been finished 
* backgroundcolor : hex code used to set the background color of the gui window
* button_color : hex code used to set the color of the gui window's buttons
* abort_button_color : hex code used to set the color of the gui window's abort (and typically error) button color
* defaultButton_color : hex code used to set the color of the gui window's default button color
* closeButton : bool used to decide if the window has a close button on the top right corner
* maximizeButton : bool used to decide if the window has a maximize/minimize button on the top rigth corner
#### 1.2 Functions
* \__init__() : Constructor; sets attributes as the user wishes and calls functions to create the window
* show() : opens a new window and sets the default button as well as its color
* center() : centers the window on the desktop
* createComponents(): creates the different components of the window; f.e. text, images, buttons ...
* createLayout() : combines the different gui elements to a layout
* createButton() : used to create a button; sets text, color, disabling functionality ...
* createPixmap() : creates a pixmap which contains an image
* createImageLabel() : creates a label which is connected to a pixmap containing an image
* get_file() : opens a window which enables the user to select a specific type of file at a specific location on the system
### 2) WindowManager
#### 2.1 Functions
* openNewWindow() : opens a new window and closes an old one if existent
* enableButtons() : enables all buttons of a gui window = makes them clickable again
* closeAll() : closes all currently opened windows of the application 
***
## example<area>.py
Demo Python file which demonstrates the basic functionalities and possibilities of this program.
A sequence of the following gui windows will give an overview over the most important aspects.
### Demo Windows
#### window1
* very basic window
* has just one button, no default, abort button or similar more complicated elements
#### window2
* is an example on how to start different threads when a button is clicked
* shows how a new window can be opened automatically after all threads have finished
* like most of the following windows it has an abort button
#### window3
* contains an image
* like in the case of most of the following windows a default button is part of this window
#### window4
* demonstrates how images and buttons can be combined in the layout
#### window5
* exemplifies the process of handling a popup window
#### window6
* exemplifies the functionality of an input field and how to retreive an user input
#### window7
* demonstrates the possibility to select a specific filetype at a specific location of the system
### Functions
#### countToX()
* dummy function used as a example on how to handle threads
* counts from 1 to X
#### printSth()
* dummy function used as a example on how to handle threads
* prints a given string
#### openPopup()
* used to open a popup window
* waits until the user clicks a button of the popup window and then closes it again
#### printInputText()
* prints the text a user entered in the input field of a gui window
#### run_threads()
* used to successively run different threads
* joins each thread before starting a new one
* optional sends finished signal after all threads have been finished
***
