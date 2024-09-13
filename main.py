from flask import Flask, request, url_for, flash, redirect,jsonify

from utils.ApiResponse import ApiResponse
from utils.ApiError import ApiError
from utils.upload_cloudinary import uploadCloudinary
from moviepy.editor import VideoFileClip
import subprocess
import os

# URLs and file names
model_url = 'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm'
scorer_url = 'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer'
model_file = 'deepspeech-0.9.3-models.pbmm'
scorer_file = 'deepspeech-0.9.3-models.scorer'

def download_file(url, filename):
    try:
        print(f"Downloading {filename} from {url}...")
        result = subprocess.run(['curl', '-LO', url], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Downloaded {filename} successfully.")
        else:
            print(f"Failed to download {filename}. Error: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


def transcribe_audio(model_path, scorer_path, audio_path, output_path):
    command = [
        'deepspeech', 
        '--model', model_path, 
        '--scorer', scorer_path, 
        '--audio', audio_path
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    with open(output_path, 'w') as f:
        f.write(result.stdout)


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
    if not video:
      return ApiError("No file found ",400)
    if video.filename=='':
      return ApiError("No file found",400)
    if video.filename[-3:]!="mp4":
      return ApiError("Not correct File format",400)
    
    #converting the received video to resolutions below:
    #we must see the original quality of the video recieved we cannot
    #better the quality we can only decrement it - sikarwar

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
    
    #building the captions feature :
    #audio to txt using google txt to speech api
    #generate captions file format
    #overlay captions on the video. -sikarwar
    
        # Check if files already exist
    if not os.path.exists(model_file):
        download_file(model_url, model_file)
    else:
        print(f"{model_file} already exists.")

    if not os.path.exists(scorer_file):
        download_file(scorer_url, scorer_file)
    else:
        print(f"{scorer_file} already exists.")

    #audio separation
    video = VideoFileClip(video_filename)
    audio = video.audio
    audio.write_audiofile("audio.wav")
    
    audio_file = 'audio.wav'
    model_file = 'deepspeech-0.9.3-models.pbmm'
    scorer_file = 'deepspeech-0.9.3-models.scorer'
    output_file = 'transcription.txt'
    
    # Transcribe audio
    transcribe_audio(model_file, scorer_file, audio_file, output_file)
    print(f"##############################################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%****************************************Transcription completed. Check '{output_file}' for the result.")
    
    for res,dim in video_resolutions.items():
      try:
        input_file = video_filename
        out_file = os.path.join(app.config['UPLOAD_FOLDER'],f"{video.filename[:-4]}_{res}.mp4")
        # print('save')
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
