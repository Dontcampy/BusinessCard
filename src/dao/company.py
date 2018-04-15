from src.utils.dbtools import Mongo

# data = {"_id": ObjectId(),
#         "uuid": "",　//客户端分配的公司uuid
#         "name": "",　//公司名
#         "isVIP": False,
#         "type": "",
#         "address": "",
#         "creator": "",
#         "create_time": time.time(),
#         "modifier": "",
#         "mod_time": time.time()}

def insert(data):
    """
    插入
    :param data: 数据 dict
    :return: None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        success = mongo.company.insert(data)
    finally:
        mongo.close()
        return success


def delete(uuid):
    """
    删除
    :param uuid: id str
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.company.remove({"uuid": uuid})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def update(uuid, new_data):
    """
    更新
    :param uuid: id str
    :param new_data: 新数据 dict
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.company.update({"uuid": uuid}, {"$set": new_data})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_id(uuid):
    """
    通过id查询
    :param uuid: str
    :return: None or dict
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.company.find_one({"uuid": uuid})
        del result["_id"]
        success = result
    finally:
        mongo.close()
        return success


def select_name(name):
    """
    通过company_name查询
    :param name: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.company.find({"name": name}):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_all():
    """
    查询
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.company.find().sort('_id', -1):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success