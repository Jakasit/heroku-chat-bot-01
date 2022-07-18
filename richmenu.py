channel_access_token ='23b+nzrs7rNbbKUyD1Otoi2bKNtGGnkRCHAtW5nwwP/1oBJWyVYJSe5Rf6M9+Clf5ayjjTHq2MCWxEDYWRTFNP+aMvTPq5YqmURtFrMUpqBF1RiFhAxMRRRM9lvKWigQbiDqreHT6iEKwCfRLdK8HgdB04t89/1O/w1cDnyilFU='
import json
from urllib import response
import requests

richdata = {
  "size": {
    "width": 2500,
    "height": 843
  },
  "selected": True,
  "name": "Rich Menu 1",
  "chatBarText": "กดเพื่อดูเมนู",
  "areas": [
    {
      "bounds": {
        "x": 1144,
        "y": 525,
        "width": 1339,
        "height": 301
      },
      "action": {
        "type": "message",
        "text": "ออกจากการสนทนา"
      }
    }
  ]
}

def RegisRich(Rich_json,channel_access_token):
    url = 'https://api.line.me/v2/bot/richmenu'
    Rich_json = json.dumps(Rich_json)
    Authorization = 'Bearer {}'.format(channel_access_token)
    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': Authorization}
    response = requests.post(url, headers=headers, data=Rich_json)
    print(str(response.json()['richMenuId']))
    return str(response.json()['richMenuId'])

def CreateRichMenu(ImageFilePath, Rich_json, channel_access_token):
    richId = RegisRich(Rich_json=Rich_json, channel_access_token=channel_access_token)
    url = 'https://api-data.line.me/v2/bot/richmenu/{}/content'.format(richId)
    Authorization = 'Bearer {}'.format(channel_access_token)
    headers = {'Content-Type': 'image/jpeg',
               'Authorization': Authorization}
    img = open(ImageFilePath, 'rb').read()
    response = requests.post(url, headers=headers, data=img)
    print(response.json())

CreateRichMenu(ImageFilePath='img_richmenu/richmenu.jpg', Rich_json=richdata,
               channel_access_token=channel_access_token)
               
# richmenu-bfceb94cf459af46c32a9cde221dc03b