import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'Paste your key here'
# Link to get Key (https://azure.microsoft.com/en-us/try/cognitive-services/my-apis/?apiSlug=face-api&country=UnitedStates&allowContact=true&fromLogin=True)

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

# Body. The URL of a JPEG image to analyze.
#body = {'url': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}
body = open('test.jpg','rb').read()
#files = {'media': open('test.jpg', 'rb')}

try:
    # Execute the REST API call and get the response.
    response = requests.request('POST', uri_base + '/face/v1.0/detect', data=body, headers=headers, params=params)

    print ('Response:')
    parsed = json.loads(response.text)
    print (json.dumps(parsed, sort_keys=True, indent=2))

except Exception as e:
    print('Error:')
    print(e)



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