
from flask import jsonify

def ApiError(message,code):
  return jsonify({
    "message":message,
    "code":code
  })