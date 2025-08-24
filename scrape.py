import asyncio
from selenium.webdriver import Firefox, FirefoxOptions
from atom import Atom
from typing import AsyncIterator


def create_firefox_driver() -> Firefox:
    """
    Establishes an instance of Firefox web driver
    
    Returns:
        (Firefox): Firefox web driver
    """
    LINK = "https://pubchem.ncbi.nlm.nih.gov/periodic-table"
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = Firefox(options=options)
    driver.get(LINK)
    return driver

def go_to_element(n: int) -> Firefox:
    if n not in range(1, 119): return None
    LINK = f"https://pubchem.ncbi.nlm.nih.gov/periodic-table/#popup={n}"
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = Firefox(options=options)
    driver.get(LINK)
    return driver

ATOM_QUERY = """
    let $rows := //div/div[2]/table/tbody/tr
"""


def value_by_xpath[T](driver: Firefox, th: str, type_: T = str) -> T | None:
    try:
        if not type_: raise ValueError
        return type_(driver.find_element(
            by="xpath",
            value=f"//div/div[2]/table/tbody/tr/th[contains(text(),'{th}')]/../td"
        ).text.split()[0])
    except Exception:
        return None

async def get_one_atom(driver: Firefox) -> Atom:
    """
    Scrape only one atom from the periodic table using CSS Selectors and XPath
    
    Parameters:
        driver (Firefox): Instance of Firefox web driver
    
    Returns:
        (Atom): Data class containing information about the periodic element
    """
    
    en = value_by_xpath(driver, "Electronegativity", float)
    yd = value_by_xpath(driver, "Year", int)
    dn = value_by_xpath(driver, "Density", float)
    a = Atom(
        number=int(driver.find_element(
            by="class name", value="text-4xl").text),
        symbol=driver.find_element(by="class name", value="text-6xl").text,
        name=driver.find_element(by="css selector", value="div.text-2xl").text,
        group=driver.find_element(
            by="css selector", value="div.text-sm.capitalize").text,
        atomicMass=float(driver.find_element(
            by="css selector",
            value="table > tbody > tr:nth-child(1) > td > a > span").text),
        standardState=driver.find_element(
            by="css selector",
            value="table > tbody > tr:nth-child(2) > td > a > span").text,
        meltingPoint= mp - 273.15 if (mp := value_by_xpath(driver, "Melting", float)) is not None else None,
        electronegativity=en,
        density=dn,
        yeardiscovered=yd
    )
    await asyncio.sleep(1)
    return a


async def scrape(driver: Firefox) -> AsyncIterator[Atom]:
    """
    Scrapes and yields the `Atom` instances from the website

    Parameters:
        driver: Instance of Firefox web driver

    Returns:
        (AsyncIterator[Atom]): Asynchronous Iterator of periodic elements
    """
    elements = driver.find_elements(by="class name", value="element")
    for element in elements:
        element.click()
        atom = await get_one_atom(driver)
        driver.find_element(by="css selector", value="button.mx-2").click()
        yield atom