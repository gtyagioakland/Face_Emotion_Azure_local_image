import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt


#*********************** Input **************************#
subscription_key = 'Paste your key here'
# Add path for the face image you want to analyse.
body = open('test.jpg','rb').read()
#*********************** Input **************************#



#******************* Azure Config ***********************#
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}


params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}




try:
    
    response = requests.request('POST', uri_base + '/face/v1.0/detect', data=body, headers=headers, params=params)
    print ('Response:')
    parsed = json.loads(response.text)
    print (json.dumps(parsed, sort_keys=True, indent=2))
except Exception as e:
    print('Error:')
    print(e)

    
#******************* Save and plot result ***********************#
f = csv.writer(open("test_result.csv", "w"))
fig, ax = plt.subplots()
df = pd.io.json.json_normalize(parsed)
df.columns = df.columns.map(lambda x: x.split(".")[-1])
df_print=df[["anger","contempt","happiness","neutral","smile"]]
print(df)
row = df_print.iloc[0]*100
row.plot(kind='bar',figsize=(10,4))
plt.show() 
df.to_csv("output.csv")

print(df)
