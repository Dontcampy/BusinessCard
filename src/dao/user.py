# Database access operations for user
from bson import ObjectId

from src.utils.dbtools import Mongo

# data = {
#     "username":"",
#     "pwd":"",
#     "admin": False,
#     "favor":[]
# }

def insert_account(username, pwd):
    """
    插入新用户
    :param username: 用户名 str
    :param pwd: 密码 str
    :return: 是否成功 None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        data = {"username": username, "pwd": pwd, "admin": False, "favor": [], "vip": True}
        success = mongo.user.insert(data)
    finally:
        mongo.close()
        return success


def del_account(_id):
    """
    :param uid: 用户id str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.remove({"_id": ObjectId(_id)})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def set_pwd(_id, pwd):
    """
    修改密码
    :param _id: 用户id str
    :param pwd: 新密码 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"_id": ObjectId(_id)}, {"$set": {"pwd": pwd}})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def set_admin(_id):
    """
    修改用户组
    :param _id: 用户id str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"_id": ObjectId(_id)}, {"$set": {"admin": True}})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_id(_id):
    """
    通过uid查找用户信息
    :param _id: 用户id str
    :return: 用户信息 list<dict> if 不为空 else ()
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.user.find_one({"_id": ObjectId(_id)})
        success = result
    finally:
        mongo.close()
        return success


def select_username(username):
    """
    通过username查找用户信息
    :param username: 用户名 str
    :return: 用户信息 list<dict> if 不为空 else ()
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.user.find_one({"username": username})
        success = result
    finally:
        mongo.close()
        return success


def push_favor(username, uuid):
    """
    给favor添加数据
    :param uuid: 名片uuid
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update_one({"username": username}, {"$push": {"favor": {"$each": [uuid], "$position": 0}}})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success

# print(insert_account("hahha", "sdaf2311"))
# insert_account("test3", "haha")
# # print(set_usergroup(4, 0))
# print(set_pwd("5accba4c30c342030033f62c", "guagua"))
# print(select_username("hahhadsfadsf"))
# push_favor("test3", "wahaha")