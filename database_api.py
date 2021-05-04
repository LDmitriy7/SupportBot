from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional


class Users(Collection):
    NAME = 'users'

    def __init__(self, db: Database):
        super().__init__(db, self.NAME)

    def set_user_tag(self, user_id: int, chan: str):
        self.update_one(
            {'uid': user_id},
            {'$set': {'uid': user_id, 'chan': chan}},
            upsert=True
        )

    def get_user_tag(self, user_id) -> Optional[str]:
        user = self.find_one({'uid': user_id})
        if not user:
            return None
        return user['chan']


class Messages(Collection):
    NAME = 'messages'

    def __init__(self, db: Database):
        super().__init__(db, self.NAME)

    def set_target_user_for(self, msg_id: int, user_id: int):
        self.replace_one(
            {'msg': msg_id},
            {'msg': msg_id, 'uid': user_id},
            upsert=True
        )

    def get_by_id(self, msg_id: int):
        return self.find_one({'msg': msg_id})

    def get_target_user_id(self, msg_id: int) -> Optional[int]:
        message = self.get_by_id(msg_id)
        if not message:
            return None
        return message['uid']


class MongoDB(Database):

    def __init__(self, name: str, client=None):
        client = client or MongoClient()
        super().__init__(client, name)

        self.users = Users(self)
        self.messages = Messages(self)
