
try:
    from pymongo.database import Database
    from pymongo.command_cursor import CommandCursor
    PYMONGO = True
except ImportError:
    Database = None
    PYMONGO = False
try:
    from motor.motor_asyncio import AsyncIOMotorDatabase
    from motor.motor_tornado import MotorDatabase
    MOTOR = True
except ImportError:
    AsyncIOMotorDatabase = None
    MotorDatabase = None
    MOTOR = False