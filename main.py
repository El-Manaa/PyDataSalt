import asyncio
from scrape import scrape, create_firefox_driver, get_one_atom, value_by_xpath, go_to_element
from dbc import connect, write_data


async def main():
    with create_firefox_driver() as driver:
        atoms = scrape(driver)
        async for atom in atoms:
            print(atom)
        # coll = connect()
        # await write_data(atoms, coll)


if __name__ == "__main__":
    asyncio.run(main())
