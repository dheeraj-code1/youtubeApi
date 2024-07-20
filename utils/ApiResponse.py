from flask import jsonify
def ApiResponse(data, message, status_code):
    return jsonify({
        "data": data,
        "message": message,
        "status_code": status_code
    })
