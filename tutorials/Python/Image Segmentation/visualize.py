'''
    Please install OpenCV and Numpy by
    pip install opencv-python
    pip install numpy
'''

import base64
import cv2
import requests
import numpy as np
import json

modelID = "MODEL_ID_HERE"
authToken = "AUTH_TOKEN_HERE"
fileName = "FILENAME_HERE"

url = "https://api.ailiverse.com/infer"

with open(fileName, "rb") as image:
  buff = base64.b64encode(image.read()).decode('utf-8')
  data = {"images" : [buff,],
          "modelID": modelID}
r = requests.post(url, 
                  data=data, 
                  headers={'Authorization': 'Bearer ' + authToken})
results = r.json()['results']['Image_Segmentation']['results']
img = cv2.imread(fileName)
for i in results:
  pts = np.array(i['contours'], np.int32)
  pts = pts.reshape((-1, 1, 2))
  image = cv2.polylines(img, [pts],
                        True, (0,0,255), 2)
  
cv2.imshow("", img)
cv2.waitKey(0)
