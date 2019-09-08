from pymongo import MongoClient


class Connection(object):
    @staticmethod
    def connect():
        client = MongoClient(host=['localhost:27017'])
        return client.Reconocimiento