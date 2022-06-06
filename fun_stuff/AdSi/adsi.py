from mailbox import mbox
import os
import ctypes
from random import randint, random
from time import sleep

UPDATES = ["https://fakeupdate.net/win10ue/",
           "https://fakeupdate.net/win10/", "https://fakeupdate.net/wnc/"]

FIREFOX = '"\\Program Files\\Mozilla Firefox\\firefox.exe" --kiosk --new-window '

MESSAGEBOXES = [18, 20]  # , 22, 36, 48, 51, 52]

SCREENSHOT = "%TEMP%\\out.png"

MB_SYSTEMMODAL = 0x00001000

# Button styles:
# 0 : OK
# 1 : OK | Cancel
# 2 : Abort | Retry | Ignore
# 3 : Yes | No | Cancel
# 4 : Yes | No
# 5 : Retry | No
# 6 : Cancel | Try Again | Continue

# To also change icon, add these values to previous number
# 16 Stop-sign icon
# 32 Question-mark icon
# 48 Exclamation-point icon
# 64 Information-sign icon consisting of an 'i' in a circle

# Button returns:
# 1 : OK
# 2 : Cancel
# 3 : Abort
# 4 : Retry
# 5 : Ignore
# 6 : Yes
# 7 : No
# 10 : Try again
# 11 : Continue

# more infos to message boxes: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox


def Mbox(title, text, style=0):
    return ctypes.windll.user32.MessageBoxExW(0, text, title, style + MB_SYSTEMMODAL)


def openKiosk(page):
    os.system(FIREFOX + page)


def messageBoxHandler(style):
    if style == 18:
        button = Mbox(
            "Ehekrise", "Es wurde eine Ehekrise entdeckt.\nWie möchted ihr mit der Ehe weiterfahren?", style)
        if button == 3:
            openKiosk("https://c.tenor.com/r7OYRTWn1C0AAAAC/kevin-hart-stare.gif")
        elif button == 4:
            Mbox("Anruf notwendig", "Ruft Claudio an.", 48)
        elif button == 5:
            Mbox("SMS gesendet",
                 "Hochzeits-OK wurde über euren Entscheid per SMS informiert.", 64)
    elif style == MESSAGEBOXES[1]:
        os.system(
            '"C:\\Program Files\\IrfanView\\i_view64.exe" /capture=1 /ini=C:\\_SWdev\\VScode\\AdSi\\ /convert=' + SCREENSHOT)
        openKiosk(SCREENSHOT)
        sleep(5)
        button = Mbox("Bildschirm Fehler",
                      "Es wurde ein Fehler mit dem Bildschirm, resp. mit dem Beamer festgestellt.\n\n Möchten Sie neu starten?", style)
        if button == 6:
            os.system("shutdown /r /t 0")
        # elif button == 7:

    # elif style == MESSAGEBOXES[2]:
    #     button = Mbox("", "", style)
    # elif style == MESSAGEBOXES[3]:
    #     button = Mbox("", "", style)
    # elif style == MESSAGEBOXES[4]:
    #     button = Mbox("", "", style)
    # elif style == MESSAGEBOXES[5]:
    #     button = Mbox("", "", style)


def randomHandler(nr):
    if nr == 0:
        openKiosk(UPDATES[0])
    elif nr == 1:
        openKiosk(UPDATES[1])
    elif nr == 2:
        openKiosk(UPDATES[2])
    elif nr == 3:
        messageBoxHandler(MESSAGEBOXES[0])
    elif nr == 4:
        messageBoxHandler(MESSAGEBOXES[1])
    elif nr == 5:
        messageBoxHandler(MESSAGEBOXES[2])
    elif nr == 6:
        messageBoxHandler(MESSAGEBOXES[3])
    elif nr == 7:
        messageBoxHandler(MESSAGEBOXES[4])
    elif nr == 8:
        messageBoxHandler(MESSAGEBOXES[5])


def hoursToSeconds(hours):
    return hours * 60 * 60


while(1):
    try:
        sleep(random()*10+10)
        randomHandler(randint(0, len(UPDATES) + len(MESSAGEBOXES) - 1))
    except KeyboardInterrupt:
        break
