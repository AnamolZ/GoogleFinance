import re
import asyncio
import time
import httpx

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import HTTPException


