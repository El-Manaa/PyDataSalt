from elementpath import select
import xml.etree.ElementTree as ET

QUERY = """
let $rows := //div/table/tbody/tr
return $rows/th[contains(text(), 'Electronegativity')]/../td
"""

tree = ET.parse("xp_test.html")
root = tree.getroot()

rows = select(root, QUERY)

print(rows)