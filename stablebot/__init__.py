import ast
import logging
import sys
from configparser import ConfigParser
from logging.handlers import TimedRotatingFileHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from stablebot.stablebot import StableBot

# Logging at the start to catch everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        TimedRotatingFileHandler('logs/stablebot.log', when="midnight", encoding=None,
                                 delay=False, backupCount=10),
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)

__version__ = '0.0.1'
__author__ = 'Athfan Khaleel'

StableBot = StableBot(__version__)

# Read from config file
name = str(StableBot).lower()
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

# Get from config file.
ADMINS = ast.literal_eval(config.get('bot', 'admins'))
LOG_GROUP = config.get('bot', 'log_group')

# MONGO_URL = config.get('mongo', 'url')
# DB_NAME = config.get('mongo', 'db_name')
# DB_USERNAME = config.get('mongo', 'db_username')
# DB_PASSWORD = config.get('mongo', 'db_password')

# Global Variables
client = None

scheduler = AsyncIOScheduler()
