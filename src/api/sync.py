import json

import src.dao.card as card
import src.dao.company as company
import src.dao.visit as visit
import src.dao.user as user
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request


class FirstSync(Resource):
    def get(self):
        token = request.args.get("token")

        if verify.verify_t(token):
            data = {"card": card.select_all(),
                    "company": company.select_all(),
                    "visit": visit.select_all()}
            return data
        else:
            return {"success": False}

class Compare(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("card")
        parser.add_argument("company")
        parser.add_argument("visit")
        parser.add_argument("token")
        args = parser.parse_args()
        # args["card"] = json.load(args["card"])
        # args["company"] = json.load(args["company"])
        # args["visit"] = json.load(args["visit"])
        username = verify.verify_t(args["token"])
        print(args)

        if username:
            # 上下行同步表结构
            sync_table = {"card": {"up": [], "down": []},
                          "company": {"up": [], "down": []},
                          "visit": {"up": [], "down": []}
                          }
            # 先对比已有的数据
            for item in args["card"]:
                data = card.select_uuid(item["uuid"])
                if data:
                    # 如果数据库中已有数据
                    if data["mod_time"] < args["mod_time"]:
                        # 如果客户端修改时间戳大于数据库修改时间戳, 将此uuid加入上传表
                        sync_table["card"]["up"].append(item["uuid"])
                    elif data["mod_time"] > args["mod_time"]:
                        # 反之加入下载表
                        sync_table["card"]["down"].append(item["uuid"])
                    else:
                        continue
                else:
                    # 如果数据库中没有数据，加入上传表
                    sync_table["card"]["up"].append(item["uuid"])
            for item in args["company"]:
                data = company.select_uuid(item["uuid"])
                if data:
                    # 如果数据库中已有数据
                    if data["mod_time"] < args["mod_time"]:
                        # 如果客户端修改时间戳大于数据库修改时间戳, 将此uuid加入上传表
                        sync_table["company"]["up"].append(item["uuid"])
                    elif data["mod_time"] > args["mod_time"]:
                        # 反之加入下载表
                        sync_table["company"]["down"].append(item["uuid"])
                    else:
                        continue
                else:
                    # 如果数据库中没有数据，加入上传表
                    sync_table["company"]["up"].append(item["uuid"])
            for item in args["visit"]:
                data = visit.select_uuid(item["uuid"])
                if data:
                    # 如果数据库中已有数据
                    if data["mod_time"] < args["mod_time"]:
                        # 如果客户端修改时间戳大于数据库修改时间戳, 将此uuid加入上传表
                        sync_table["visit"]["up"].append(item["uuid"])
                    elif data["mod_time"] > args["mod_time"]:
                        # 反之加入下载表
                        sync_table["visit"]["down"].append(item["uuid"])
                    else:
                        continue
                else:
                    # 如果数据库中没有数据，加入上传表
                    sync_table["visit"]["up"].append(item["uuid"])
            # 返回同步表
            return sync_table
        return {False}


class Download(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("card")
        parser.add_argument("company")
        parser.add_argument("visit")
        parser.add_argument("token")
        args = parser.parse_args()

        if verify.verify_t(args["token"]):
            result = {"card": [],
                      "company": [],
                      "visit": []}
            # 通过uuid查询需要发给客户端的数据并加入result
            for uuid in args["card"]:
                result["card"].append(card.select_uuid(uuid))
            for uuid in args["company"]:
                result["company"].append(company.select_uuid(uuid))
            for uuid in args["company"]:
                result["visit"].append(visit.select_uuid(uuid))
            return result
        return {False}


class Upload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("card")
        parser.add_argument("company")
        parser.add_argument("visit")
        parser.add_argument("token")
        args = parser.parse_args()

        if verify.verify_t(args["token"]):
            for item in args["card"]:
                # item = json.load(item)
                card.update(item["uuid"], item)
            for item in args["company"]:
                # item = json.load(item)
                company.update(item["uuid"], item)
            for item in args["visit"]:
                # item = json.load(item)
                visit.update(item["uuid"], item)
            return {True}
        return {False}