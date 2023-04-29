import PySimpleGUI as sg
import cv2
import numpy as np

def popup(site,wn):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text(site)],
                #[sg.Text('Enter something on Row 2'), sg.InputText()],
                [sg.Button('Accept'), sg.Button('Negate'), sg.Button('Whitelist'), sg.Button('Blacklist')] ]

    # Create the Window
    window = sg.Window('Auth #'+str(wn), layout)
    # Event Loop to process "events" and get the "values" of the inputs
    ret = 'N'
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Accept':
            ret = 'A'
            break
        if event == sg.WIN_CLOSED or event == 'Negate':
            break
        if event == sg.WIN_CLOSED or event == 'Whitelist':
            ret = 'W'
            break
        if event == sg.WIN_CLOSED or event == 'Blacklist':
            ret = 'B'
            break
    window.close()
    return ret

def popup_cv2(site,wn):
    image = np.zeros((200,500,3))
    fthick, fsize = 2, 0.7
    offset = 45
    text = cv2.putText(image, site, (10,30), cv2.FONT_HERSHEY_SIMPLEX, fsize, (255,255,255), fthick, cv2.LINE_AA)
    cline = 0
    
    cline +=1
    image = cv2.putText(image, "[A] - Accept", (20,offset+30*cline), cv2.FONT_HERSHEY_SIMPLEX, fsize, (255,255,0), fthick, cv2.LINE_AA)
    cline +=1
    image = cv2.putText(image, "[N] - Negate", (20,offset+30*cline), cv2.FONT_HERSHEY_SIMPLEX, fsize, (255,0,255), fthick, cv2.LINE_AA)
    cline +=1
    image = cv2.putText(image, "[W] - Whitelist", (20,offset+30*cline), cv2.FONT_HERSHEY_SIMPLEX, fsize, (0,255,0), fthick, cv2.LINE_AA)
    cline +=1
    image = cv2.putText(image, "[B] - Blacklist", (20,offset+30*cline), cv2.FONT_HERSHEY_SIMPLEX, fsize, (0,0,255), fthick, cv2.LINE_AA)
    cv2.imshow('Auth #'+str(wn), image)
    answers = ['A','N','W','B']
    ans = ''
    while not(ans in answers):
        key = cv2.waitKey(0)
        ans = chr(int(key)).upper()
        #print(ans)
    return ans

def popup_text(site,wn):
    ans = input('Choose an option for',site,':>').upper()
    return ans

def popup_descr(site,wn,data):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    todisplay = data[:]
    layout = [  [sg.Text(site)],
                [sg.Multiline(todisplay, size=(50, 10), disabled=True)],
                [sg.Button('Accept'), sg.Button('Negate'), sg.Button('Whitelist'), sg.Button('Blacklist')] ]

    # Create the Window
    window = sg.Window('Auth #'+str(wn), layout)
    # Event Loop to process "events" and get the "values" of the inputs
    ret = 'N'
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Accept':
            ret = 'A'
            break
        if event == sg.WIN_CLOSED or event == 'Negate':
            break
        if event == sg.WIN_CLOSED or event == 'Whitelist':
            ret = 'W'
            break
        if event == sg.WIN_CLOSED or event == 'Blacklist':
            ret = 'B'
            break
    window.close()
    return ret

cwn = 0
if __name__ == "__main__":
    
    print('starting!')
    cwn += 1
    data = 'nel mezzo del cammin di nostra vitaaaaaaaaaaaaaaaaaaaaa\nmi ritrovai per una selva oscura'
    data = data +'\n'+data
    data = data +'\n'+data
    data = data +'\n'+data
    ans = popup_descr('www.example.com', cwn, data)
    print('Auth #'+str(cwn)+' result:',ans)
    print('ending!')