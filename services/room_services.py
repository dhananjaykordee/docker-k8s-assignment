import json


class RoomService:

    @staticmethod
    def get_rooms():

        with open("rooms.json", "r") as file:
            return json.load(file)

    @staticmethod
    def get_room_by_id(room_id):

        with open("rooms.json", "r") as file:

            rooms = json.load(file)

        for room in rooms:

            if room["id"] == room_id:
                return room

        return None
