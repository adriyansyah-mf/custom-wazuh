#!/usr/bin/env python3

import sys
import requests
import json

"""
ossec.conf configuration structure
 <integration>
     <name>custom-discord</name>
     <hook_url>https://discord.com/api/webhooks/1147505445339140186/u2cNtmN1OXOXZSnd3W4Zi8e74eKfiykk78kA7W_bZXRqgVbbscfgEttI6FGy9buOxMG3</hook_url>
     <alert_format>json</alert_format>
 </integration>
"""

# read configuration
alert_file = sys.argv[1]
user = sys.argv[2].split(":")[0]
hook_url = sys.argv[3]

# read alert file
with open(alert_file) as f:
    alert_json = json.loads(f.read())

# extract alert fields
alert_level = alert_json["rule"]["level"]

if alert_level < 5:
    # green
    color = "5763719"
elif 5 <= alert_level <= 7:
    # yellow
    color = "16705372"
else:
    # red
    color = "15548997"

try:
    source_ip = alert_json["data"]["srcip"]
except KeyError:
    source_ip = "N/A"

try:
    destination_ip = alert_json["agent"]["ip"]
except KeyError:
    destination_ip = "N/A"

try:
    timestamps = alert_json["predecoder"]["timestamp"]
except KeyError:
    timestamps = "N/A"

# agent details
if "agentless" in alert_json:
    agent_ = "agentless"
else:
    agent_ = alert_json["agent"]["name"]

# combine message details
payload = json.dumps({
    "content": "",
    "embeds": [
        {
            "title": f"Wazuh Alert - Rule {alert_json['rule']['id']}",
            "color": int(color),  # Convert color to int
            "description": alert_json["rule"]["description"],
            "fields": [
                {
                    "name": "Agent",
                    "value": agent_,
                    "inline": True
                },
                {
                    "name": "Source IP",
                    "value": source_ip,
                    "inline": True
                },
                {
                    "name": "Destination IP",
                    "value": destination_ip,
                    "inline": True
                },
                {
                    "name": "Timestamps",
                    "value": timestamps,
                    "inline": True
                }
            ]
        }
    ]
})

# send message to discord
try:
    response = requests.post(hook_url, data=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()  # Raise an error for bad HTTP status
except requests.exceptions.RequestException as e:
    print(f"Failed to send notification: {e}")
    sys.exit(1)

sys.exit(0)
