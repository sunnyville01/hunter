import json
import time
import sqlite3
import requests
from os import path
import urllib.request
from coins import Coins
from operator import itemgetter


conn = sqlite3.connect('hunter.db')
c = conn.cursor()
