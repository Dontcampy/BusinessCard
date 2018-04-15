import re
import base64
import os

import shortuuid

from flask_restful import Resource, reqparse

from .error import ERROR_0, ERROR_1, ERROR_3, ERROR_4
from src.utils.verify import verify_t, verify_arguments


class UploadImg(Resource):
    def post(self):
        result = {"success": False}
        ver_list = ['token', 'img', 'imgFormat']
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('img')
        parser.add_argument('imgFormat')

        args = parser.parse_args()

        # 验证必要参数完整性
        if verify_arguments(ver_list, args) is False:
            result["error"] = ERROR_1
            return result

        # 验证
        uid = verify_t(args["token"])
        if uid:
            # 正则表达式处理imgdata
            pattern = r'data:image/(.*);base64,(.*)'

            s = re.search(pattern, args['img'])
            # 将图片解码并保存至images文件夹
            try:
                image_data = base64.b64decode(s.group(2))
                image_name = shortuuid.uuid() + "." + s.group(1)
                image_path = os.path.abspath(os.path.join('/var/www/html/images', image_name))
                with open(image_path, 'wb') as imageFile:
                    imageFile.write(image_data)

                image_url = 'images/' + image_name
                result["success"] = True
                result["imgURL"] = image_url
            except Exception as e:
                print(e)
                result["error"] = ERROR_4
                return result
            return result
        else:
            result["error"] = ERROR_3
            return result
