'''
    This is the demo script for performing Image Classification using Ailiverse APIs
'''

import requests
import json
import base64

email = 'YOUR_EMAIL_ADDRESS'                        # Email Address for registering
password = "YOUR_PASSWORD"                          # Password for registering
organization = "YOUR_ORGANIZATION"                  # Organization Name

SIGN_IN_URL = "https://api.ailiverse.com/signIn"
CREATE_MODEL_URL = "https://api.ailiverse.com/createModel"
UPLOAD_URL = "https://api.ailiverse.com/userUpload"
STATUS_URL = "https://api.ailiverse.com/status"
TRAIN_URL = "https://api.ailiverse.com/train"
INFER_URL = "https://api.ailiverse.com/infer"

'''
    Method for registering a user on Ailiverse API.
    It will return an authentication token.
    Input Parameters:
        - email: required
        - password: required
        - organization: optional
    Output:
        - authToken
'''
SIGN_UP_URL = "https://api.ailiverse.com/signUp"
data =  { "email": email,
          "password": password,
          "confirm_password": password,
          "organization": organization }

r = requests.post(SIGN_UP_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
authToken = r.json()['authToken']

# Uncomment if your email is already registered, however, you've lost your token
# '''
#     Method for logging in (in case you lost your Authentication Token) on Ailiverse API.
#     Input Parameters:
#         - email: required
#         - password: required
#     Output:
#         - authToken
# '''
# data =  { "email": email, "password": password }
# r = requests.post(SIGN_IN_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
# authToken = r.json()['authToken']


'''
    Method for registering a model using the API
    Input Parameters:
        - model_type: required
        - Authorization: required
    Output:
        - modelID
'''
data =  { "model_type": "Image_Classification"}
r = requests.post(CREATE_MODEL_URL, data=json.dumps(data), headers={'Authorization': 'Bearer ' + authToken})
modelID = r.json()['modelID']

'''
    Method for uploading a compressed file
    Input Parameters:
        - file: required
        - Authorization: required
        - modelID: required
    Output:
        - Uploads the dataset to Ailiverse Servers
'''
paths = {"file": open("train.zip", "rb")}
data =  {"modelID": modelID }
r = requests.post(url=UPLOAD_URL, data=data, files=paths, headers={'Authorization': 'Bearer ' + authToken})
print(r.json())

'''
    Method for starting training
    Input Parameters:
        - Authorization: required
        - modelID: required
        - epochs: optional
    Output:
        - Starts Training
'''
data =  {"epochs": 10, "modelID": modelID}
r = requests.post(url=TRAIN_URL, data=json.dumps(data), headers={"Authorization": "Bearer " + authToken})
print(r.json())

'''
    Method for checking status of training after it has been initialized.
    The loop ends when training is Done
'''
while True:
    r = requests.get(STATUS_URL, params={"modelID": modelID},
                    headers={"Content-type": "application/json",
                            "Authorization": "Bearer " + authToken})
    print(r.json())
    if (r.json()['training'] == 'Done'):
        break

'''
    Performing an Inference on a single image
'''
print("Running Inference", modelID, authToken)
with open("hen.jpg", "rb") as image:
    buff = base64.b64encode(image.read()).decode('utf-8')
    data = {"images" : [buff,],
            "modelID": modelID}
    r = requests.post(INFER_URL,
                      data=data,
                      headers={"Authorization": "Bearer " + authToken})
    print(r.json())
