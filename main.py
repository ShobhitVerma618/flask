from flask import Flask, jsonify, request , make_response
from flask_restful import Api
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pymongo
from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
from flask_cors import CORS


cloudinary.config(
  cloud_name = "dy1hexft1",
  api_key = "311744991862889",
  api_secret = "2uq-b8O_1WMASu06UY5Kj5WsLmg",
  secure = True
)

myFont = ImageFont.truetype('calibri.ttf', size=40)

def makeCertificate(data):
    W, H = (1920,1080)
    msg = data['name']
    im = Image.open('cert.png')
    draw = ImageDraw.Draw(im)
    _, _, w, h = draw.textbbox((1100, 500),msg, font=myFont)
    draw.text(((W-w)/2, (H-h)/2), msg,font=myFont,fill='orange')

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
def hello_world():
    data = request.json
    #print(data['name'])
    #p_id = data['id']
    makeCertificate(data)
    #insertIntoDatabase(data)
    url = uploadImage()
    res = make_response(jsonify({"url": url}))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
