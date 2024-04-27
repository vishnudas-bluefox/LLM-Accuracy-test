import asyncio

from csv_processor import CSVProcessor

async def main():
    processor = CSVProcessor('data.csv')
    results = await processor.read_and_print_csv()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
