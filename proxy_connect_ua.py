import socket
import sys
from _thread import *
import ssl 
import os
from blacklist_rules import check_url
import time
import PySimpleGUI as sg

default_ua_1 = b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
default_ua_2 = b'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0'
custom_ua = b'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'

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

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32


#based on: https://github.com/mrprofessor/MinimalPythonProxy

listening_port = 8000
max_connection = 5
buffer_size = 8192

fb = open('blacklist.txt','r')
blacklist = fb.read().splitlines()
fb.close()

fcl = open('connections.txt','w+')
fcl.write('list of connections...\n')

fca = open('accepted.txt','w+')
fca.write('[ACCEPTED] connections:\n')

fcb = open('blocked.txt','w+')
fcb.write('[BLOCKED] connections:\n')

uw = open('user_whitelist.txt','r')
user_whitelist = uw.read().splitlines()
uw.close()

ub = open('user_blacklist.txt','r')
user_blacklist = ub.read().splitlines()
ub.close()


zombie_socket_max_time = 0.005
tcwn = 0

def popup_text(site,wn):
    tans = input(Colors.YELLOW + 'Choose an option for '+ Colors.END + Colors.CYAN + site + Colors.END + Colors.YELLOW + ' :>  ' + Colors.END )
    tans = tans.upper()
    print(tans)
    return tans

def change_ua(data, old_ua, new_ua):
    return data[:].replace(old_ua, new_ua)

def start():    #Main Program
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listening_port))
        sock.listen(max_connection)
        print("[*] Server started successfully [ %d ]" %(listening_port))
    except Exception:
        print("[*] Unable to Initialize Socket")
        print(Exception)
        sys.exit(2)
        
    while True:
        try:
                conn, addr = sock.accept() #Accept connection from client browser
                data = conn.recv(buffer_size).replace(b'CONNECT',b'GET') #Recieve client data
                data = change_ua(data, default_ua_1, custom_ua)
                data = change_ua(data, default_ua_2, custom_ua)
                print(Colors.BROWN + '[CONNECTING]' + Colors.END)
                thr_isaccepted, thr_isHTTPS, thr_webserver, thr_port, thr_conn, thr_addr = conn_string(conn, data, addr)
                start_new_thread(conn_thread, (thr_isaccepted, thr_isHTTPS, thr_webserver, thr_port, thr_conn, thr_addr, data)) #Starting a thread
        except KeyboardInterrupt:
            sock.close()
            print("\n[*] Graceful Shutdown")
            fcl.close()
            fca.close()
            fcb.close()
            sys.exit(1)
        except:
            print(Colors.RED + '[ERROR]' + Colors.END)
            pass

def conn_string(conn, data, addr):
    
    print(Colors.LIGHT_CYAN + data[:].decode().strip('\n').strip('\r\n') + Colors.END)
    first_line = data.split(b'\n')[0]
    
    method = first_line.split()[0]
    url = first_line.split()[1]
    
    http_pos = url.find(b'://') #Finding the position of ://
    if(http_pos==-1):
        temp=url
    else:
        temp = url[(http_pos+3):]
    
    port_pos = temp.find(b':')
    
    webserver_pos = temp.find(b'/')
    if webserver_pos == -1:
        webserver_pos = len(temp)
    
    webserver = ""
    port = -1
    isHTTPS = False
    if(port_pos == -1 or webserver_pos < port_pos):
        port = 80 #HTTP
        #port = 443 #HTTPS
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]
    if port==443:
        isHTTPS=True
    
    str_webserver = webserver[:].decode()
    isaccepted = False
    if not(str_webserver in blacklist) and not(str_webserver in user_blacklist) and check_url(str_webserver):
        if str_webserver in user_whitelist:
            isaccepted = True
        else:
            print(50*'#')
            
            global tcwn
            tcwn += 1
            print('Auth #', tcwn)
            #ans = popup_text(str_webserver, 1*tcwn)
            #ans = popup(str_webserver, 1*tcwn)
            ans = popup_descr(str_webserver, 1*tcwn, data[:].decode().strip('\n').strip('\r\n'))
            if ans == 'A':
                print(Colors.CYAN + '[ACCEPTED] '+ Colors.END + str_webserver + Colors.CYAN +' Accepted!' + Colors.END)
                isaccepted = True
            if ans == 'N':
                print(Colors.PURPLE + '[NEGATED] '+ Colors.END + str_webserver + Colors.PURPLE +' Negated!' + Colors.END)
                isaccepted = False
            if ans == 'W':
                print(Colors.GREEN + '[WHITELISTED] '+ Colors.END + str_webserver + Colors.GREEN +' Whitelisted!' + Colors.END)
                isaccepted = True
                user_whitelist.append(str_webserver)
                uw = open('user_whitelist.txt','w+')
                uw.write('\n'.join(user_whitelist))
                uw.close()
            if ans == 'B':
                print(Colors.RED + '[BLACKLISTED] '+ Colors.END + str_webserver + Colors.RED +' Blacklisted!' + Colors.END)
                isaccepted = False
                user_blacklist.append(str_webserver)
                ub = open('user_blacklist.txt','w+')
                ub.write('\n'.join(user_blacklist))
                ub.close()
    
    if isaccepted:
        print(Colors.GREEN + "[ALLOWED]" + Colors.END, Colors.CYAN + str_webserver + Colors.END,'is currently connecting...')
        fcl.write('[ALLOWED] '+str_webserver+' is currently connecting...\n')
        fca.write('[ALLOWED] '+str_webserver+'\n')
    else:
        print(Colors.RED + "[BLOCKED] " + Colors.END, Colors.PURPLE + str_webserver + Colors.END,'is currently blocked!\n')
        fcl.write('[BLOCKED] '+str_webserver+' is currently blocked!\n')
        fcb.write('[BLOCKED] '+str_webserver+'\n')
    return [isaccepted, isHTTPS, webserver, port, conn, addr]


def conn_thread(isaccepted, isHTTPS, webserver, port, conn, addr, data):
    try:
        str_webserver = webserver[:].decode()
        if isaccepted:
            if isHTTPS:
                proxy_server_https(webserver, port, conn, addr, data)
            else:
                proxy_server(webserver, port, conn, addr, data)
            print(Colors.LIGHT_CYAN + data[:].decode() + Colors.END)
        #proxy_server(webserver, port, conn, addr, data) #HTTP
        #proxy_server_https(webserver, port, conn, addr, data) #HTTPS
    except Exception:
        pass

#based on answer: https://stackoverflow.com/questions/24218058/python-https-proxy-tunnelling
def proxy_server_https(webserver, port, conn, addr, data):
    
    try:
        print(data[:].decode())
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock = ssl.wrap_socket(usock, ssl_version=ssl.PROTOCOL_TLSv1)  #HTTPS 
        sock.connect((webserver, port))
        reply = "HTTP/1.0 200 Connection established\r\n"
        reply += "Proxy-agent: Pyx\r\n"
        reply += "\r\n"
        conn.sendall( reply.encode() )
        #sock.send(data)
        
        
        print(Colors.YELLOW + '#####  HTTPS connect to: '+ Colors.END + Colors.CYAN + webserver[:].decode() + Colors.END + Colors.YELLOW + '   #####' + Colors.END)
        print(Colors.LIGHT_BLUE + data[:150].decode() + Colors.END)
        
       
        # Indiscriminately forward bytes
        conn.setblocking(0)
        sock.setblocking(0)
        
        ztime = time.time()
        zte = 0.0
        
        while True:
            
            try:
                request = conn.recv(buffer_size)
                sock.sendall( request )
                dar = len(request)
                if dar>0:
                        ztime = time.time()
                ctime = time.time()
                zte = round(ctime - ztime,3)
                dar = str(dar)
                dar = "%s B" % (dar)
                print(Colors.LIGHT_GREEN + "[*] HTTPS:" + Colors.END,"%s %s %s || => %s <= | ztime: %s" % (Colors.YELLOW + webserver[:].decode() + Colors.END, Colors.PURPLE+">>>"+Colors.END, str(addr[0]), str(dar),Colors.YELLOW+str(zte)+Colors.END))
            except socket.error as err:
                pass
            
            try:
                reply = sock.recv(buffer_size)
                conn.sendall( reply )
                dar = len(reply)
                if dar>0:
                        ztime = time.time()
                ctime = time.time()
                zte = round(ctime - ztime,3)
                dar = str(dar)
                dar = "%s B" % (dar)
                print(Colors.LIGHT_GREEN + "[*] HTTPS:" + Colors.END,"%s %s %s || => %s <= | ztime: %s" % (Colors.YELLOW + webserver[:].decode() + Colors.END, Colors.CYAN+"<<<"+Colors.END, str(addr[0]), str(dar), Colors.YELLOW+str(zte)+Colors.END))
            except socket.error as err:
               pass
            if zte>zombie_socket_max_time:
                break
    except socket.error:
        sock.close()
        conn.close()
        print(sock.error)
        sys.exit(1)

def proxy_server(webserver, port, conn, addr, data):
    try:
        print(Colors.LIGHT_CYAN + data[:].decode() + Colors.END)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock = ssl.wrap_socket(usock, ssl_version=ssl.PROTOCOL_TLSv1)  #HTTPS 
        sock.connect((webserver, port))
        sock.send(data)
        
        flag_init = True
        ztime = time.time()
        zte = 0.0
        while 1:
            reply = sock.recv(buffer_size)
            
            
            if(len(reply)>0):
                conn.send(reply)
                
                dar = len(reply)
                if dar>0:
                        ztime = time.time()
                ctime = time.time()
                zte = round(ctime - ztime,3)
                dar = str(dar)
                dar = "%s B" % (dar)
                print("[*] Request Done: %s >> %s || => %s <= | ztime: %s" % (str(webserver),str(addr[0]), str(dar), Colors.YELLOW+str(zte)+Colors.END))
            
            
            if flag_init:
                print(Colors.LIGHT_GREEN + '#####   connected to: '+ Colors.END + Colors.CYAN + webserver[:].decode() + Colors.END + Colors.LIGHT_GREEN + '   #####' + Colors.END)
                print(Colors.LIGHT_CYAN + reply[:150].decode() + Colors.END)
                flag_init = False
            else:
                break
            if zte>zombie_socket_max_time:
                break
        sock.close()
        
        conn.close()
    except socket.error:
        sock.close()
        conn.close()
        print(sock.error)
        sys.exit(1)



if __name__== "__main__":
    start()