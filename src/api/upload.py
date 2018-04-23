import re
import base64
import os

import shortuuid
import werkzeug.datastructures

from flask_restful import Resource, reqparse

from .error import ERROR_4


class UploadImg(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()

        # 将图片解码并保存至images文件夹
        try:
            file = args["image"]
            file.save(os.path.join('/usr/share/nginx/html/images', file.filename))
            image_url = 'images/' + file.filename
            result["success"] = True
            result["imgURL"] = image_url
        except Exception as e:
            print(e)
            result["error"] = ERROR_4
            return result
        return result
