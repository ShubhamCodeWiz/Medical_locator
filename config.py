import os

class Config:
    SECRET_KEY = '34rjkfis439jf3jladfmo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_equipment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False