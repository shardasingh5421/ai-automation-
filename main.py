"""
main.py
Main entrypoint for ESG Risk Analyzer. Coordinates asyncio loops and concurrency limits.
"""

import asyncio
from typing import Dict
from tqdm.asyncio import tqdm_asyncio

import config
from logger import logger
from csv_handler import init_output_csv, load_pending_companies, save_result
from llm_client import analyze_company

async def process_company(
    company: Dict[str, str], 
    semaphore: asyncio.Semaphore, 
    csv_lock: asyncio.Lock,
    pbar: tqdm_asyncio
) -> None:
    """Worker task that limits concurrency, sleeps for rate limits, and saves data."""
    async with semaphore:
        c_name = company["company_name"]
        c_sector = company["sector"]
        c_country = company["country"]
        
        # Rate Limiting Protection
        await asyncio.sleep(config.RATE_LIMIT_SLEEP)
        
        logger.info(f"Analyzing {c_name}...")
        
        # Fetch Analysis
        result = await analyze_company(c_name, c_sector, c_country)
        
        row_data = {
            "company_name": c_name,
            "sector": c_sector,
            "country": c_country,
            **result
        }
        
        # Coroutine-safe write
        async with csv_lock:
            save_result(row_data)
            
        pbar.update(1)

async def main_async() -> None:
    """Main asynchronous pipeline orchestrator."""
    logger.info("Initializing Output CSV...")
    init_output_csv()
    
    pending_companies = load_pending_companies()
    if not pending_companies:
        logger.info("All companies have already been processed.")
        print("All caught up! Output is located in esg_risk_output.csv")
        return
        
    logger.info(f"Starting async processing for {len(pending_companies)} companies.")
    
    semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_REQUESTS)
    csv_lock = asyncio.Lock()
    
    pbar = tqdm_asyncio(total=len(pending_companies), desc="Processing ESG Risks")
    
    tasks = [
        process_company(company, semaphore, csv_lock, pbar)
        for company in pending_companies
    ]
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)
    
    pbar.close()
    logger.info("Pipeline processing completed.")

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
        print(f"\nProcessing complete! Output saved to: {config.OUTPUT_CSV}")
    except KeyboardInterrupt:
        print("\nProcess interrupted. Progress saved.")
        logger.warning("Pipeline interrupted by user.")
    except Exception as e:
        print(f"\nA critical failure occurred: {str(e)}")
        logger.exception("Critical error in main.")
