from datetime import datetime
from dotenv import load_dotenv
from time import time
import os
import urllib3
import json

load_dotenv()

headers = {
    "Cookie" : os.getenv("COOKIE")
}

model_id = int(input("Enter Model id: "))
final_version = int(input("Enter version you will go up to: "))
# rbxm or rbxl

print("TYPE 'M' for model or type 'L' for place")

filetype_extension = input()

filetype_extension = filetype_extension.lower()

filetype_validation = (filetype_extension is None) or (filetype_extension != "l" and filetype_extension != "m") or len(filetype_extension) > 1

if filetype_validation:
    filetype_extension = "m"

for version in range(1, final_version + 1):
    u = f"https://assetdelivery.roblox.com/v2/assetId/{model_id}/version/{version}"
    r_data = urllib3.request("GET", url=u, headers=headers)
    decoded_data = r_data.data.decode("utf-8")
    json_coded = json.loads(decoded_data)
    version_url = json.dumps(json_coded["locations"][0]["location"])

    v_data = urllib3.request("GET", url=version_url.replace('"', ""))
    date_str = v_data.info().getheaders("Last-Modified")[0]
    
    stripped_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    unix_stamp = stripped_time.timestamp()
    with open(f"output/{model_id}-v{version}.rbx{filetype_extension}", "wb") as f:
        f.write(v_data.data)
    os.utime(f"output/{model_id}-v{version}.rbx{filetype_extension}", (time(), unix_stamp))
    
