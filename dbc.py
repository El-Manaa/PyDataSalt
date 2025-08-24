from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from os import getenv
from typing import AsyncIterator


def connect() -> Collection | None:
    """Establishes a Connection to MongoDB

    Returns:
        (pymongo.collection.Collection | None): Collection of `Periodic/Chemical Elements`
    """
    load_dotenv()
    URL = getenv("MG_URL")
    client = MongoClient(URL, server_api=ServerApi("1"))
    try:
        return client[getenv("CLIENT")].get_collection(getenv("COLL"))
    except Exception as e:
        print(e)
        return None


def read_data[T](c: Collection | None) -> AsyncIterator[T] | None:
    """
    Reads data from the Collection `c` and asynchronously **yields** it in a generic type `T` instance.

    Parameters:
        c (Collection | None): MongoDB Collection (if it exists) from MongoDB

    Returns:
        (AsyncIterator[T] or None): Optional asynchronous Iterator of `T` 
    """
    if c is None:
        return None
    else:
        return (T(**data) for data in c.find())  # type: ignore []


async def write_data[T](ld: AsyncIterator[T] | None, c: Collection | None) -> None:
    """
    Writes the data generated from the Iterator `ld` into the Collection `c`

    Parameters:
        ld (AsyncIterator[T] or None): Asynchronous Iterator of `T`
        c (Collection or None): Optional MongoDB Collection
    """
    if ld is not None and c is not None:
        # I would use **Monads** 😞
        async for d in ld:
            c.insert_one(d.__dict__)


def add_one[T](a: T, c: Collection | None) -> None:
    """Inserts one instance's data to the collection

    Parameters:
        a (T): instance to insert
        c (Collection | None): MongoDB Collection 
    """
    if c is not None:
        c.insert_one(a.__dict__)
