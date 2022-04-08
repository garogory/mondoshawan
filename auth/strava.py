
CLIENT_ID = "56300"
CLIENT_SECRET = "98a56b33b19f4fca66658eeb63381ccde348239a"
ACCESS_TOKEN = "022c5569642df52510147a65e10c6af4bd6efa17"
UPDATE_TOKEN = "c325a5255dc851cac78b11c1fb6e9ac21f47832b"

CODE = "554251068ab465a003df347e8b4cf5dee877ef01"

import requests
import json
# Make Strava auth API call with your
# client_code, client_secret and code
response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': CLIENT_ID,
                            'client_secret': CLIENT_SECRET,
                            'code': CODE,
                            'grant_type': 'authorization_code'
                            }
                )
#Save json response as a variable
strava_tokens = response.json()
# Save tokens to file
with open('strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)
# Open JSON file and print the file contents
# to check it's worked properly
with open('strava_tokens.json') as check:
  data = json.load(check)
print(data)
