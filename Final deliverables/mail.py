from mailjet_rest import Client
import os
api_key = '71ccb22303b75f55a1e4592f6fe367e8'
api_secret = 'b2413e0c9f02e44e895032fd13c1800b'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "plasmadonorapplication@protonmail.com",
        "Name": "Sathish"
      },
      "To": [
        {
          "Email": "plasmadonorapplication@protonmail.com",
          "Name": "Sathish"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())