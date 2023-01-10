'''
    This is the demo script for performing Text Guided Image Segmentation using Ailiverse APIs
'''

import requests
import base64
import json

email = 'YOUR_EMAIL_ADDRESS'                        # Email Address for registering
password = "YOUR_PASSWORD"                          # Password for registering
organization = "YOUR_ORGANIZATION"                  # Organization Name

SIGN_IN_URL = "http://34.80.13.82:8085/signIn"
CREATE_MODEL_URL = "http://34.80.13.82:8085/createModel"
INFER_URL = "http://34.80.13.82:8085/infer"

# '''
#     Method for registering a user on Ailiverse API.
#     It will return an authentication token.
#     Input Parameters:
#         - email: required
#         - password: required
#         - organization: optional
#     Output:
#         - authToken
# '''
# SIGN_UP_URL = "http://34.80.13.82:8085/signUp"
# data =  { "email": email,
#           "password": password,
#           "confirm_password": password,
#           "organization": organization }

# r = requests.post(SIGN_UP_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
# authToken = r.json()['authToken']

# Uncomment if your email is already registered, however, you've lost your token
'''
    Method for logging in (in case you lost your Authentication Token) on Ailiverse API.
    Input Parameters:
        - email: required
        - password: required
    Output:
        - authToken
'''
data =  { "email": email, "password": password }
r = requests.post(SIGN_IN_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
authToken = r.json()['authToken']
 
'''
    Method for registering a model using the API
    Input Parameters:
       - model_type: required
       - Authorization: required
    Output:
    - modelID
    '''
data =  { "model_type": "Text_Guided_Segmentation"}
r = requests.post(CREATE_MODEL_URL, data=json.dumps(data), headers={'Authorization': 'Bearer ' + authToken})
print(r.json())
modelID = r.json()['modelID']

'''
    Performing an Inference on a single image
'''
print("Running Inference", modelID, authToken)
with open("hen.jpg", "rb") as image:
    buff = base64.b64encode(image.read()).decode('utf-8')
    data = {"images" : buff,
            "texts": ["Hen"],
            "modelID": modelID}
    r = requests.post(INFER_URL,
                      data=data,
                      headers={"Authorization": "Bearer " + authToken})
    print(r.json())