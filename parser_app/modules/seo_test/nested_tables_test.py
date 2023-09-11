import requests
from bs4 import BeautifulSoup


def has_nested_tables(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        # Find all table elements
        table_elements = soup.select("table")
        # Check for nested tables
        nested_tables = 0
        for table in table_elements:
            parent_tables = table.find_parents("table")
            if parent_tables:
                nested_tables += 1
                selector_parts = []
                current_element = table
                while current_element:
                    if current_element.name == 'body':
                        break
                    if current_element.name:
                        element_selector = current_element.name
                        # print(element_selector)
                        if current_element.get("id"):
                            element_selector += f'#{current_element.get("id")}'
                        if current_element.get("class"):
                            element_selector += f'.{".".join(current_element.get("class"))}'
                        selector_parts.insert(0, element_selector)
                    current_element = current_element.parent
                print(selector_parts)
                # selector = " ".join(selector_parts)
                # nested_table_selectors.append(selector)
                # print(selector)
        if nested_tables > 0:
            print(f"The page has {nested_tables} nested table(s).")
            return [f"The page has {nested_tables} nested table(s).", selector_parts]
        else:
            print("The page does not have nested tables.")
            return ["The page does not have nested tables.", ['-']]

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# # Replace this with the URL you want to check
# url_to_check = "https://www.javatpoint.com/html-nested-table"
# print(has_nested_tables(url_to_check))


def nested_tables_test(link):
    return [has_nested_tables(link)]
