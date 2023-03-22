
from flask import Flask, jsonify, request , make_response ,Response
from flask_restful import Api
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
from quart_cors import cors
from flask_cors import CORS
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1i-o7Otisc2vAqJ_Yi8OoE6mKiMt1xGDBlXmOGEBxVAs'
SAMPLE_RANGE_NAME = 'A1:AA1000'


def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

main()
def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)
    
    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None
        
# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('client.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])

def Export_Data_To_Sheets(df1):
    response_date = service.spreadsheets().values().update(
        spreadsheetId='1i-o7Otisc2vAqJ_Yi8OoE6mKiMt1xGDBlXmOGEBxVAs',
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict(
            majorDimension='ROWS',
            values=df1.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated')

cloudinary.config(
  cloud_name = "dy1hexft1",
  api_key = "311744991862889",
  api_secret = "2uq-b8O_1WMASu06UY5Kj5WsLmg",
  secure = True
)

myFont = ImageFont.truetype('calibri.ttf', size=40)

async def uploadGoogleSheets(data):
    main()
    df=pd.DataFrame(values_input[1:], columns=values_input[0])
    df1=df[:]
    print(df)
    df2 = {'Name': data['name'],'Email':data['email'],'Phone':data['phone'] ,'Instagram Profile Link':data['instagram'],'City':data['city'],'Answer to radio box':data['radio'],'Remarks':data['remarks']}
    df1 = df1.append(df2, ignore_index = True)
    Export_Data_To_Sheets(df1)
    print(df)  

def makeCertificate(data):
    W = 1920 
    H2 = 1080
    msg = data['name']
    im = Image.open('cert.png')
    draw = ImageDraw.Draw(im)
    _, _, w, h = draw.textbbox((1100, 500),msg, font=myFont)
    draw.text(((W-w)/2, (H2-h)/2), msg,font=myFont,fill='orange')

    im.save("hello5.png", "PNG")

def uploadImage():

  # Upload the image and get its URL
  # ==============================

  # Upload the image.
  # Set the asset's public ID and allow overwriting the asset with new versions
  response = cloudinary.uploader.upload("hello5.png", public_id="fasdfaf", unique_filename = False, overwrite=True)
  #print(response)
  # Build the URL for the image and save it in the variable 'srcURL'
  srcURL = response['secure_url']

  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
  return srcURL

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
async def hello_world():
    data = request.get_json()
    print(data)
    #p_id = data['id']
    makeCertificate(data)
    #insertIntoDatabase(data)
    url = uploadImage()
    await uploadGoogleSheets(data)
    res = make_response(jsonify({"url": url}))
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


if __name__ == '__main__':
    app.run(debug=True, port=3001)
