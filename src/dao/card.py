from src.utils.dbtools import Mongo

# data = {"_id": ObjectId(),
#         "uuid": "", //客户端分配的uuid
#         "name": "", //姓名
#         "phone": "",
#         "company_uuid": "uuid", //公司uuid
#         "company_name": "", //公司名
#         "position": "",
#         "address": "",
#         "creator": "", //创建者
#         "create_time": time.time(), //创建时间戳
#         "modifier": "", //修改者
#         "mod_time": time.time()} //修改时间戳


def insert(data):
    """
    插入名片
    :param data: 名片数据 dict
    :return: None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        success = mongo.card.insert(data)
    finally:
        mongo.close()
        return success


def delete(uuid):
    """
    删除名片
    :param uuid: 名片id str
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.card.remove({"uuid": uuid})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def update(uuid, new_data):
    """
    更新名片
    :param uuid: 名片id str
    :param new_data: 新数据 dict
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.card.update({"uuid": uuid}, {"$set": new_data})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_uuid(uuid):
    """
    通过uuid查询
    :param uuid: str
    :return: None or dict
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.card.find_one({"uuid": uuid})
        del result["_id"]
        success = result
    finally:
        mongo.close()
        return success


def select_name(name):
    """
    通过name查询
    :param name: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"name": name}):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_company(company):
    """
    通过company_name查询
    :param name: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"company_name": company}):
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
        for item in mongo.card.find().sort('_id', -1):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success