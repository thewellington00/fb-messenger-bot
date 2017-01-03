from app import db

class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.Unicode)

class Last_Message(db.Model):
    __tablename__ = "last_message"
    id = db.Column('id', db.Integer, primary_key=True)
    fb_uid = db.Column('fb_uid', db.Integer)
    last_user_message = db.Column('last_user_message', db.Unicode)
    last_bot_response = db.Column('last_bot_response', db.Unicode)

class Bus_Stops(db.Model):
    __tablename__ = "bus_stops"
    id = db.Column('id', db.Integer, primary_key=True)
    fb_uid = db.Column('fb_uid', db.Integer)
    stop_custom_name = db.Column('stop_custom_name', db.Unicode)
    stop_id = db.Column('stop_id', db.Unicode)

class Car_Locations(db.Model):
    __tablename__ = "car_locations"
    id = db.Column('id', db.Integer, primary_key=True)
    current_location = db.Column('current_location', db.Unicode)
    last_location = db.Column('last_location', db.Unicode)


