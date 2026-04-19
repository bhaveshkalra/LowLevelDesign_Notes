"""
Here there are N given meeting rooms. Book a meeting in any meeting room at given interval (starting time, end time). 
Also send notifications to all person who are invited for meeting.
You should use calender for tracking date and time. And also history of all the meetings which are booked and meeting room. 
Write an API for client who will give date and time, and API should return meeting room with booked scheduled time. 
Client should also query for history of last 20 booked meetings.
"""

"""
Functional =>
Book meeting room with (start_time, end_time)
Check room availability
Return available rooms for given slot
Maintain meeting history (last 20)
Send notifications to participants
Calendar-based scheduling

Non-Functional =>
No double booking (Critical)
Scalable for multiple rooms/users
Low latency availability check
"""


from datetime import datetime
from collections import deque


class Meeting:
    def __init__(self, meeting_id, room_id, start_time, end_time, participants):
        self.meeting_id = meeting_id
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants


class MeetingRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.bookings = []  #List of Meetings (sorted by start_time)


class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email


class Calendar:
    @staticmethod
    def is_overlap(start1, end1, start2, end2):
        return not (end1 <= start2 or start1 >= end2)


class MeetingRoomService:
    def __init__(self):
        self.rooms = {}  # room_id -> MeetingRoom

    def is_room_available(self, room, start, end):
        for meeting in room.bookings:
            if Calendar.is_overlap(start, end, meeting.start_time, meeting.end_time):
                return False
        return True

    def get_available_rooms(self, start, end):
        available = []
        for room in self.rooms.values():
            if self.is_room_available(room, start, end):
                available.append(room)
        return available

    def book_room(self, room, meeting):
        if not self.is_room_available(room, meeting.start_time, meeting.end_time):
            raise Exception("Room not available")

        room.bookings.append(meeting)
        room.bookings.sort(key=lambda x: x.start_time)


class NotificationService:
    def send_notification(self, participants, meeting):
        for user in participants:
            print(f"Notify {user.email} about meeting {meeting.meeting_id}")


class MeetingHistory:
    def __init__(self):
        self.history = deque(maxlen=20)

    def add(self, meeting):
        self.history.appendleft(meeting)

    def get_last_20(self):
        return list(self.history)


import uuid

class MeetingSchedulerSystem:
    def __init__(self):
        self.room_service = MeetingRoomService()
        self.notification_service = NotificationService()
        self.history = MeetingHistory()

    # API: Get available rooms
    def get_available_rooms(self, start, end):
        return self.room_service.get_available_rooms(start, end)

    # API: Book meeting
    def book_meeting(self, start, end, participants):
        rooms = self.get_available_rooms(start, end)
        if not rooms:
            raise Exception("No rooms available")

        room = rooms[0]  # pick first available
        meeting_id = str(uuid.uuid4())

        meeting = Meeting(meeting_id, room.room_id, start, end, participants)

        self.room_service.book_room(room, meeting)
        self.history.add(meeting)
        self.notification_service.send_notification(participants, meeting)

        return meeting

    # API: Check availability
    def is_room_available(self, room_id, start, end):
        room = self.room_service.rooms.get(room_id)
        return self.room_service.is_room_available(room, start, end)

    # API: Get last 20 meetings
    def get_meeting_history(self):
        return self.history.get_last_20()


"""Concurrency Handling
DB transaction / row-level locking
Optimistic locking

Scaling
Cache available rooms
Partition by building/location
"""
