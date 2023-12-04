import re
import asyncio
import time
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import HTTPException
from GFinanceOAuth import get_current_user

STOCK_SYMBOLS = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "GOOG", "NVDA", "NFLX"]
DATA = {}

async def fetch_stock_data(client, semaphore, stock):
    start_time = time.time()
    async with semaphore:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        url = f'https://www.google.com/finance/quote/{stock}:NASDAQ'

        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            target_div = soup.find('div', class_='YMlKec fxKbKc')

            if target_div:
                stock_price = float(target_div.text.strip()[1:])
                page_title = soup.title.text
                stock_name = page_title.split('Stock')[0].strip()
                stock_symbol_short = re.search(r'\((.*?)\)', stock_name).group(1)
                DATA[stock_symbol_short] = stock_price

            end_time = time.time()
            final_time = end_time - start_time
            if final_time > 2:
                return

        except httpx.RequestError as exc:
            print(f'Failed to retrieve the page for {stock}. {exc}')

async def validate_access_token(token: str):
    try:
        current_user = await get_current_user(token=token)
        return current_user
    except HTTPException as exc:
        return exc

async def fetch_all_stocks(stock_symbols):
    semaphore = asyncio.Semaphore(8)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_stock_data(client, semaphore, stock) for stock in stock_symbols]
        await asyncio.gather(*tasks)
    print(DATA)

if __name__ == "__main__":
    MAX_ATTEMPTS = 3
    for attempt in range(1, MAX_ATTEMPTS + 1):
        token_input = input("Enter your access token: ")

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(validate_access_token(token_input))

        if isinstance(result, HTTPException):
            print(f"Access denied!")
            if attempt == MAX_ATTEMPTS:
                print("Maximum attempts reached.")
                break
            else:
                print(f"Attempt {attempt}/{MAX_ATTEMPTS}. Please try again.")
        else:
            print("Access granted!")
            while True:
                loop.run_until_complete(fetch_all_stocks(STOCK_SYMBOLS))
