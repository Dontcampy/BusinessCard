from src.utils.dbtools import Mongo

# data = {"_id": ObjectId(),
#         "uuid": "", //客户端分配的uuid
#         "owner_uuid": "uuid", //创建这条拜访记录的公司的uuid
#         "company": "", //拜访公司名
#         "aim": "", // 目的
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
        success = mongo.visit.insert(data)
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
        result = mongo.visit.remove({"uuid": uuid})
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
        result = mongo.visit.update({"uuid": uuid}, {"$set": new_data})
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
        result = mongo.visit.find_one({"uuid": uuid})
        del result["_id"]
        success = result
    finally:
        mongo.close()
        return success


def select_owner(owner_uuid):
    """
    owner_uuid
    :param owner_uuid: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.visit.find({"owner_uuid": owner_uuid}).sort('_id', -1):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success