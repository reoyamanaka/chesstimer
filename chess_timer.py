import time, threading, wx, os, sys
from subprocess import call
from os import system

#Creating a window for my program with a specified title and size
app = wx.App()
window = wx.Frame(None, title = "Reo's Chess Timer", size = (700,400))
panel = wx.Panel(window)
popup = wx.Frame(None, title = "Time's up!", size = (200, 150))
startTimeEntry = wx.Frame(None, title = "Start Time Entry", size = (330, 130))
initialPanel = wx.Panel(startTimeEntry)

#Function to close the main window
def closeWindow(event):
    window.Destroy()
    os._exit(0)

#start time
startTime = 0.000001
whiteTime = 0.000001
blackTime = 0.000001

#startTimeEntry design
def initialSet(event):
    global startTime, whiteTime, blackTime, whiteRemainingTime, blackRemainingTime, timerThread
    startTime = initialInput.GetValue()
    whiteTime = float(startTime)
    blackTime = float(startTime)
    whiteRemainingTime = wx.StaticText(panel, label = "Remaining time: \n%d seconds" %whiteTime, pos = (50, 40))
    whiteRemainingTime.SetFont(labelFont)
    blackRemainingTime = wx.StaticText(panel, label = "Remaining time: \n%d seconds" %blackTime, pos = (400, 40))
    blackRemainingTime.SetFont(labelFont)

    startTimeEntry.Hide()
    window.Show(True)

    timerThread = threading.Thread(target = double_timer)
    timerThread.start()

initialLabel = wx.StaticText(initialPanel, label = "Enter how long each player has total in seconds.", pos = (20, 10))
initialInput = wx.TextCtrl(initialPanel, pos = (145, 37), size = (35, 25))
initialButton = wx.Button(initialPanel, label = "Confirm", pos = (122, 75))
initialButton.Bind(wx.EVT_BUTTON, initialSet)

#Function to close the popup
def hidePopup(event):
    popup.Hide()

#font options
labelFont = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
buttonFont = wx.Font(19, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
popupFont = wx.Font(38, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

#icons
whiteIcon = wx.Bitmap("white.png", wx.BITMAP_TYPE_ANY)
blackIcon = wx.Bitmap("black.png", wx.BITMAP_TYPE_ANY)

whiteIconPic1 = wx.StaticBitmap(panel, -1, whiteIcon, pos = (5, 275))
whiteIconPic2 = wx.StaticBitmap(panel, -1, whiteIcon, pos = (50, 275))
whiteIconPic3 = wx.StaticBitmap(panel, -1, whiteIcon, pos = (95, 275))

blackIconPic1 = wx.StaticBitmap(panel, -1, blackIcon, pos = (600, 275))
blackIconPic2 = wx.StaticBitmap(panel, -1, blackIcon, pos = (555, 275))
blackIconPic3 = wx.StaticBitmap(panel, -1, blackIcon, pos = (510, 275))

#White
whiteLabel = wx.StaticText(panel, label = "White", pos = (50, 10))
whiteLabel.SetFont(labelFont)

#Black
blackLabel = wx.StaticText(panel, label = "Black", pos = (400, 10))
blackLabel.SetFont(labelFont)

turn = 0
paused = 1

def double_timer():
    global whiteTime, blackTime
    global whiteRemainingTime, blackRemainingTime
    global turn, paused
    while whiteTime > 0 and blackTime > 0:
        if turn == 0 and paused == 0:
            whiteTime = whiteTime - 1
            whiteRemainingTime.SetLabel("Remaining time: \n%d seconds" %whiteTime)

        elif turn == 1 and paused == 0:
            blackTime = blackTime - 1
            blackRemainingTime.SetLabel("Remaining time: \n%d seconds" %blackTime)

        time.sleep(1)

    if paused == 0:
        popup.Show(True)
        call(["osascript -e 'set volume output volume 50'"], shell = True)
        if whiteTime <= 0:
            pass
            #system("say White side, your time is up!")
        if blackTime <= 0:
            pass
            #system("say Black side, your time is up!")

def switchTurn(event):
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0     
    
def startGame(event):
    global paused
    paused = 0

def pauseGame(event):
    global paused
    paused = 1

def resetTimer(event):
    global paused, turn, whiteRemainingTime, blackRemainingTime, whiteTime, blackTime
    paused = 1
    turn = 0
    whiteTime = 0
    blackTime = 0
    startTimeEntry.Show(True)
    initialInput.Clear()
    window.Hide()
    whiteRemainingTime.SetLabel("")
    blackRemainingTime.SetLabel("")


#startButton
startButton = wx.Button(panel, label = "Start", pos = (240, 230), size = (200, 50))
startButton.Bind(wx.EVT_BUTTON, startGame)
startButton.SetFont(buttonFont)

#switchButton
switchButton = wx.Button(panel, label = "Switch", pos = (140, 160), size = (400, 50))
switchButton.Bind(wx.EVT_BUTTON, switchTurn)
switchButton.SetFont(buttonFont)

#Button to pause the game
pauseButton = wx.Button(panel, label = "Pause", pos = (240, 260), size = (200, 50))
pauseButton.Bind(wx.EVT_BUTTON, pauseGame)
pauseButton.SetFont(buttonFont)

#Button to reset timer
resetButton = wx.Button(panel, label = "Reset", pos = (240, 290), size = (200, 50))
resetButton.Bind(wx.EVT_BUTTON, resetTimer)
resetButton.SetFont(buttonFont)

#Button to close the window
quitButton = wx.Button(panel, label = "Close", pos = (240, 320), size = (200, 50))
quitButton.Bind(wx.EVT_BUTTON, closeWindow)
quitButton.SetFont(buttonFont)

#label and button for the "Time's up!" popup frame
popupNote = wx.StaticText(popup, label = "Time's up!", pos = (3, 20))
popupNote.SetFont(popupFont)


popupButton = wx.Button(popup, label = "Okay", pos = (60, 90))
popupButton.Bind(wx.EVT_BUTTON, hidePopup)

startTimeEntry.Show(True)
app.MainLoop()
