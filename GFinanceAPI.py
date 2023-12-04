import re
import asyncio
import time
import httpx

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import HTTPException

from GFinanceAPI import get_current_user

stockSymbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "GOOG", "NVDA", "NFLX"]

data={}
async def fetch_data(client, semaphore, stock):
    start_time = time.time()
    async with semaphore:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        url = f'https://www.google.com/finance/quote/{stock}:NASDAQ'

        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            targetDiv = soup.find('div', class_='YMlKec fxKbKc')

            if targetDiv:
                stockPrice = float(targetDiv.text.strip()[1:])
                pageTitle = soup.title.text
                stockName = pageTitle.split('Stock')[0].strip()
                stockSymbolShort = re.search(r'\((.*?)\)', stockName).group(1)
                data[stockSymbolShort] = stockPrice

            end_time = time.time()
            final_time = end_time - start_time
            if final_time >2:
                return 

        else:
            print(f'Failed to retrieve the page for {stock}. Status code: {response.status_code}')

async def validate_token(token: str):
    try:
        current_user = await get_current_user(token=token)
        return current_user
    except HTTPException as exc:
        return exc

async def fetch_all_stocks(stock_symbols):
    semaphore = asyncio.Semaphore(8)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, semaphore, stock) for stock in stock_symbols]
        await asyncio.gather(*tasks)
    print(data)

