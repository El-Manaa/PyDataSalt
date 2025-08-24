import asyncio
from scrape import scrape, create_firefox_driver
from dbc import connect, write_data


async def main():
    with create_firefox_driver() as driver:
        atoms = scrape(driver)
        coll = connect()
        await write_data(atoms, coll)


if __name__ == "__main__":
    asyncio.run(main())
