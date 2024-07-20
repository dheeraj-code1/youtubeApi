import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

import os
from dotenv import load_dotenv

load_dotenv()
# Configuration       
cloudinary.config( 
    cloud_name = "di3dtztfm", 
    api_key = os.getenv('API_KEY'), 
    api_secret = os.getenv('API_SECERT'),
    secure=True
)

def uploadCloudinary(file_name):
  return cloudinary.uploader.upload(file_name,
  resource_type = "video")
  