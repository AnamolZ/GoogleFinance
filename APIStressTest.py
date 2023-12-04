import asyncio
import concurrent.futures
from GFinanceAPI import fetch_all_stocks, validate_access_token
from fastapi import HTTPException
import time

async def main():
    MAX_THREADS = 20
    STOCK_SYMBOLS = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "GOOG", "NVDA", "NFLX"]

    token_input = input("Enter your access token: ")

    loop = asyncio.get_event_loop()
    start_time = time.time()
    result = await validate_access_token(token_input)
    end_time_validate = time.time()

    if isinstance(result, HTTPException):
        print(f"Access denied! {result.detail}")
    else:
        print(f"Access granted! Time taken for validation: {end_time_validate - start_time:.2f} seconds")

        futures = []
        start_time_fetch = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for _ in range(MAX_THREADS):
                future = loop.run_in_executor(executor, asyncio.run, fetch_all_stocks(STOCK_SYMBOLS))
                futures.append(future)

            try:
                results = await asyncio.gather(*futures)
                end_time_fetch = time.time()

                all_data = {}
                for data in results:
                    if data:
                        all_data.update(data)

                print(f"Time taken for fetching all stocks: {end_time_fetch - start_time_fetch:.2f} seconds")
                print(f"Total time taken for stress test: {end_time_fetch - start_time:.2f} seconds")
                print(f"Overall performance: {len(STOCK_SYMBOLS) * MAX_THREADS / (end_time_fetch - start_time):.2f} requests per second")

            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
