# Database access operations for user
from bson import ObjectId

from src.utils.dbtools import Mongo


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
        data = {"username": username, "pwd": pwd, "admin": False, "favor": [], "vip": True,
                "avatar": "", "section": "", "position": ""}
        success = mongo.user.insert(data)
    except Exception as e:
        raise e
    finally:
        mongo.close()
        return success


def del_account(username):
    """
    :param username: 用户名 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.remove({"username": username})
        success = bool(result["n"])
    except Exception as e:
        raise e
    finally:
        mongo.close()
        return success


def set_pwd(username, pwd):
    """
    修改密码
    :param username: 用户名 str
    :param pwd: 新密码 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"username": username}, {"$set": {"pwd": pwd}})
        success = bool(result["n"])
    except Exception as e:
        raise e
    finally:
        mongo.close()
        return success


def set_admin(username):
    """
    修改用户组
    :param username: 用户名 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"username": username}, {"$set": {"admin": True}})
        success = bool(result["n"])
    except Exception as e:
        raise e
    finally:
        mongo.close()
        return success


def set_info(username, avatar, section, position):
    """
    修改信息
    :param avatar: 头像文件名 str
    :param section: 部门 str
    :param position: 职位 str
    :return:
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"username": username},
                                   {"$set": {"avatar": avatar, "section": section, "position": position}})
        success = bool(result["n"])
    except Exception as e:
        raise e
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
    except Exception as e:
        raise e
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
    except Exception as e:
        raise e
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
    except Exception as e:
        raise e
    finally:
        mongo.close()
        return success
