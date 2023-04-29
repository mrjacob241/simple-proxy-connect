

def check_microsoft(url, vsflag = False):
    if ("microsoft" in url):
        if vsflag and ("visualstudio.microsoft.com" in url):
            return True
        else:
            return False
    else:
        return True

def check_mcafee(url):
    if "mcafee" in url:
        return False
    else:
        return True

def check_google(url,allow_maps=False):
    if ("google" in url) and not(("www.google.it" == url) or ("www.google.com" == url) or ("googlevideo" in url)):
        if (("maps.google.com" == url) and allow_maps):
            return True
        else:
            return False
    else:
        return True

def check_hp(url):
    if "hp." in url:
        return False
    else:
        return True

def check_globalsign(url):
    if "globalsign" in url:
        return False
    else:
        return True

def check_adobe(url):
    if "adobe" in url:
        return False
    else:
        return True

def check_onedrive(url):
    if (("oneclient" in url) or ("onedrive" in url)):
        return False
    else:
        return True

def check_glive(url):
    if "g.live" in url:
        return False
    else:
        return True

def check_teams(url):
    if "teams" in url:
        return False
    else:
        return True

def check_office(url):
    if "office" in url and not("libreoffice" in url):
        return False
    else:
        return True

def check_msftconnecttest(url):
    if "msftconnecttest" in url:
        return False
    else:
        return True

def check_skype(url):
    if "skype" in url:
        return False
    else:
        return True

def check_beacons(url):
    if "beacons" in url:
        return False
    else:
        return True

def check_spotify(url):
    if "spotify" in url:
        return False
    else:
        return True

def check_msn(url):
    if "msn" in url:
        return False
    else:
        return True

def check_windows(url):
    if "windows" in url:
        return False
    else:
        return True

def check_bing(url):
    if "bing" in url:
        return False
    else:
        return True

def check_edge(url):
    #Exception
    if "twitch.tv" in url:
        return True
    if ("ttvnw.net" in url) and ("video-edge" in url):
        return True
    
    if "edge" in url:
        return False
    else:
        return True

def check_x1(url): #x1.c.lencr.org
    if ("lencr.org" in url) or ("x1.c.lencr" in url):
        return False
    else:
        return True

def check_akamaihd(url): #spoprod-a.akamaihd.net
    if ("akamaihd.net" in url):
        return False
    else:
        return True

def check_aayinltcs(url): #evs.aayinltcs.arduino.cc
    if ("evs.aayinltcs.arduino.cc" in url):
        return False
    else:
        return True

def check_algolia(url): #y2y10mz7jy-dsn.algolia.net, y2y10mz7jy-2.algolianet.com
    if ("algolia.net" in url) or ("algolianet.com" in url):
        return False
    else:
        return True

def check_cloudfront(url): #dr3fr5q4g2ul9.cloudfront.net
    if ("cloudfront" in url):
        return False
    else:
        return True

def check_telemetry(url): #dr3fr5q4g2ul9.cloudfront.net
    if ("telemetry" in url):
        return False
    else:
        return True

def check_analytics(url): #dr3fr5q4g2ul9.cloudfront.net
    if ("analytics" in url):
        return False
    else:
        return True

def check_xboxlive(url): 
    if ("xboxlive" in url):
        return False
    else:
        return True

def check_anydesk(url): 
    if ("anydesk" in url):
        return False
    else:
        return True

def check_url(url):
    valid = True
    ### BEGIN bootup NordVPN ###
    valid = valid and check_globalsign(url)
    valid = valid and check_google(url, allow_maps=False)
    ### END bootup NordVPN ###
    valid = valid and check_glive(url)
    valid = valid and check_microsoft(url, vsflag=False)
    valid = valid and check_mcafee(url)
    valid = valid and check_hp(url)
    valid = valid and check_adobe(url)
    valid = valid and check_onedrive(url)
    valid = valid and check_teams(url)
    valid = valid and check_office(url)
    valid = valid and check_msftconnecttest(url)
    valid = valid and check_skype(url)
    valid = valid and check_beacons(url)
    valid = valid and check_spotify(url)
    valid = valid and check_msn(url)
    valid = valid and check_windows(url)
    valid = valid and check_bing(url)
    valid = valid and check_edge(url)
    valid = valid and check_x1(url)
    valid = valid and check_akamaihd(url)
    valid = valid and check_aayinltcs(url)
    valid = valid and check_algolia(url)
    valid = valid and check_cloudfront(url)
    valid = valid and check_telemetry(url)
    valid = valid and check_analytics(url)
    valid = valid and check_anydesk(url)
    
    return valid