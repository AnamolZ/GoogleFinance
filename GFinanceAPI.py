import re
import asyncio
import time
import httpx

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import HTTPException

from GFinanceAPI import get_current_user

data={}
async def fetch_data(client, semaphore, stock):
    start_time = time.time()
    async with semaphore:
        


