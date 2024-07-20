from flask import Flask, request, url_for, flash, redirect,jsonify

from utils.ApiResponse import ApiResponse
from utils.ApiError import ApiError
from utils.upload_cloudinary import uploadCloudinary
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/video/",methods=['POST'])
def video_quality():
  # check file is empty
  # check extension
  # reduce quality 144p,240p,360p,480p
  # save on these local
  # upload these on cloudinary
  # delete from locals 
  if request.method =='POST':
      
    video = request.files['file']
    if video.filename=='':
      return ApiError("No file found",400)
    if video.filename[-3:]!="mp4":
      return ApiError("Not correct File format",400)
    
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
    
    video_resolutions = {
      "1080p": (1920, 1080),
      "720p": (1280, 720),
      "480p": (640, 480),
      "360p": (640, 360),
      "240p": (426, 240),
      "144p": (256, 144)  
    }
    resp ={}
    video_filename = os.path.join(app.config['UPLOAD_FOLDER'],video.filename)
    for res,dim in video_resolutions.items():
      try:
        input_file = video_filename
        out_file = os.path.join(app.config['UPLOAD_FOLDER'],f"{video.filename[:-4]}_{res}.mp4")
        clip = VideoFileClip(input_file)
        resized_clip = clip.resize(dim)
        resized_clip.write_videofile(out_file)
        
        file_uploaded = uploadCloudinary(out_file)
        # print(file_uploaded)
        resp[res] = file_uploaded["url"]
        if os.path.exists(out_file):
          os.remove(out_file)
 
      except Exception as e:
        print(e)
        # return ApiError(e,400)
    if os.path.exists(video_filename):
      os.remove(video_filename)
    return ApiResponse(resp,"success",200)