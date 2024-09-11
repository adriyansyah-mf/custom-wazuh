import json
import requests
import sys
payload = json.dumps({
    "content": "",
    "embeds": [
        {
            "title": "Wazuh Alert - Rule",
            "description": "test",
            "fields": [
                {
                    "name": "Agent",
                    "value": "007",
                    "inline": True
                },
                {
                    "name": "Source IP",
                    "value": "3333333",
                    "inline": True
                },
                {
                    "name": "Destination IP",
                    "value": "5555555",
                    "inline": True
                },
                {
                    "name": "Timestamps",
                    "value": "N/A",  # Changed from None to "N/A"
                    "inline": True
                }
            ]
        }
    ]
})


# send message to discord
r = requests.post("https://discord.com/api/webhooks/1147505445339140186/u2cNtmN1OXOXZSnd3W4Zi8e74eKfiykk78kA7W_bZXRqgVbbscfgEttI6FGy9buOxMG3", data=payload, headers={"content-type": "application/json"})
sys.exit(0)