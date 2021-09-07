import json
import requests
import time

url = "https://api.symbl.ai/v1/process/text"

f = open("input.txt", "r")
text = f.read()

payload = {
    "name": "Business Meeting",  # <Optional,String| your_meeting_name by default conversationId>

    "confidenceThreshold": 0.5,
    # <Optional,double| Minimum required confidence for the insight to be recognized. Value ranges between 0.0 to 1.0. Default value is 0.5.>

    "detectPhrases": True,
    # <Optional,boolean| It shows Actionable Phrases in each sentence of conversation. These sentences can be found using the Conversation's Messages API. Default value is false.>

    "messages": [
        {
            "duration": {"startTime": "2020-07-21T16:04:19.99Z", "endTime": "2020-07-21T16:04:20.99Z"},
            # <Optional, object| Duration object containing startTime and/or endTime for the transcript.>, e.g.
            "payload": {
                "content" : text,
                "contentType": "text/plain"
            }
        }
    ]
}

def get_access_token():
    urlAuth = "https://api.symbl.ai/oauth2/token:generate"

    appId = "32336c49503638557257456b31514143525346457975696d4138675252453666"  # App Id found in your platform
    appSecret = "69715843717673736c6e654d623932674558766a64665a4774783951743039424c52694c544e6a49315a39313038725472514b41486a747370314c55476e724d"  # App Id found in your platform

    payload = {
        "type": "application",
        "appId": appId,
        "appSecret": appSecret
    }
    headers = {
        'Content-Type': 'application/json'
    }

    authresponse = requests.request("POST", urlAuth, headers=headers, data=json.dumps(payload))
    # set your access token here. See https://docs.symbl.ai/docs/developer-tools/authentication
    return authresponse.json()["accessToken"]

# set your access token here. See https://docs.symbl.ai/docs/developer-tools/authentication
access_token = get_access_token()

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

responses = {
    400: 'Bad Request! Please refer docs for correct input fields.',
    401: 'Unauthorized. Please generate a new access token.',
    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
    429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
    500: 'Something went wrong! Please contact support@symbl.ai'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

time.sleep(10)

baseUrl = "https://api.symbl.ai/v1/conversations/{conversationId}/topics"
conversationId = response.json()['conversationId']  # Generated using Submit text end point

url1 = baseUrl.format(conversationId=conversationId)

headers1 = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

params1 = {
    'sentiment': True,  # <Optional, boolean| Give you sentiment analysis on each topic in conversation.>
}

responses1 = {
    401: 'Unauthorized. Please generate a new access token.',
    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
    500: 'Something went wrong! Please contact support@symbl.ai'
}

response1 = requests.request("GET", url1, headers=headers1, params=json.dumps(params1))

if response1.status_code == 200:
    # Successful API execution
    print("topics => " + str(response1.json()['topics']))  # topics object containing topics id, text, type, score, messageIds, sentiment object, parentRefs
elif response1.status_code in responses1.keys():
    print(responses1[response1.status_code])  # Expected error occurred
else:
    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response1.text))

exit()
