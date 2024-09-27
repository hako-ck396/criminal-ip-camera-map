from rich import print
from rich.console import Console
from rich.panel import Panel
import geocoder
import requests
import folium
import os

def check_api_key(key):
    url = "https://api.criminalip.io/v1/user/me"
    payload = {}
    headers = {"x-api-key": key}
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        if response.status_code != 200:
            return False, None
        response = response.json()
        name = response["data"]["name"]
        return True, name
    except:
        return False, None

g = geocoder.ip("me")
city = g.city
latlng = g.latlng
console = Console()
console.clear()
console.print(
    Panel(f"Criminal ip Camera Map\n\n you are in [red]{city}[/red]", style="bold"), justify="center", style="bold"
)
CIP_API_KEY = input("Enter your Criminal IP API key: ")
if check_api_key(CIP_API_KEY) == (False, None):
    console.print("Invalid API Key", style="bold red")
    exit()

ips = []
with console.status("[bold green]Looking for IP Camera for your city", spinner="dots"):
    url = f"https://api.criminalip.io/v1/banner/search?query=city:{city} tag:IP Camera&offset=0"
    payload = {}
    headers = {"x-api-key": CIP_API_KEY}
    response = requests.request("GET", url, headers=headers, data=payload)
    for i in response.json()["data"]['result']:
        ips.append(i["ip_address"])

m = folium.Map(location=[latlng[0], latlng[1]], zoom_start=16, tiles="cartodbpositron")
popup_html = """
<b style="font-size:20px;">Camera Inpos</b><br>
"""

for ip in ips:
    popup_html += f'<a href="https://www.criminalip.io/asset/report/{ip}" target="_blank" style="font-size:18px;">{ip}</a><br>'

popup_html += f'<br><br><a href="https://www.criminalip.io/asset/search?query=city%3A+{city}+tag%3A+IP+Camera" target="_blank" style="font-size:18px;">More Camera in {city}</a><br>'

folium.Marker(
    location=[latlng[0], latlng[1]],
    popup=folium.Popup(popup_html, max_width=600),
    tooltip="Show Details",
).add_to(m)

m.save("criminal_ip_camera_map.html")

print("🌏 Done 🌏")
dir_path = os.path.dirname(os.path.realpath(__file__))
print()
print("Open the address below with your browser")
print("file://" + dir_path + "/criminal_ip_camera_map.html")
