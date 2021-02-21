import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from web_elements import Elements

delay = 3


def open_browser():
    browser = webdriver.Chrome()
    return browser


def navigate_to_amazon():
    driver.maximize_window()
    driver.get('https://www.amazon.com/')
    try:
        search = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, Elements.nav_search))
        )
        print("Amazon is loaded!")
        return search
    except TimeoutException:
        print("Loading took too much time!")


def search_for_item(search_field):
    search_field.click()
    search_field.send_keys('Star Wars')
    search_field.submit()
    try:
        department_menu = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, Elements.departments))
        )
        if department_menu:
            return department_menu
    except TimeoutException:
        print('All Departments menu not found!')


def select_all_department(all_departments):
    if all_departments:
        all_departments.click()
    else:
        pass
    try:
        toys_and_games = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, Elements.toys_departments))
        )
        return toys_and_games
    except TimeoutException:
        print('Toys and Games department not found')


def select_page_two_button(select_department):
    select_department.click()
    next_button = WebDriverWait(driver, delay).until(EC.visibility_of_element_located(
        (By.XPATH, Elements.select_next_button))
    )
    next_button.click()


def select_first_product_of_page_two():
    product = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, Elements.select_item))
    )
    return product


def extract_number(text):
    p = re.compile("(\d+\.?\d+)")
    result = p.search(text)
    return float(result.group(1))


def get_price_and_qty(select_product):
    select_product.click()
    in_stock = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="availability"]/span'))
    ).text
    if in_stock == 'In Stock.':
        pass
    else:
        print('The selected item is unavailable for purchase!')
        driver.back()

    get_price = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, Elements.item_price))
    ).text
    qty = driver.find_element_by_xpath(Elements.quantity_dropdown)
    qty.click()

    qty_options = driver.find_elements_by_xpath(Elements.select_value_options)
    path = Elements.dropdown_option.format(len(qty_options) - 1)

    select_number_of_item = driver.find_element_by_xpath(path).text
    if select_number_of_item:
        select_value = driver.find_element_by_xpath(path)
        select_value.click()
    return extract_number(get_price), int(select_number_of_item)


def get_product_title():
    title = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, Elements.product_title))
    ).text
    return title


def add_product_to_cart():
    add_to_cart = driver.find_element_by_xpath(Elements.add_to_cart)
    add_to_cart.click()


def select_cart_button():
    cart = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, Elements.cart_button))
    )
    cart.click()


def get_subtotal_amount():
    get_subtotal = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, Elements.subtotal_amount))
    ).text
    return extract_number(get_subtotal)


def get_product_title_in_cart():
    shopping_cart_prod_title = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, Elements.cart_product_title))
    ).text
    return shopping_cart_prod_title


def assert_items(product_title, item_title_in_cart):
    if str(product_title) == str(item_title_in_cart):
        print("The names is the same!", str(product_title), str(item_title_in_cart))
        return True
    else:
        print('Not the same', str(product_title), str(item_title_in_cart))
        return False


def assert_prices(item_price, quantity, subtotal):
    if item_price * quantity == subtotal:
        print("The subtotal is equal to the price multiplied by the quantity")
        return True
    else:
        print('The subtotal is NOT equal to the price multiplied by the quantity')
        return False


if __name__ == '__main__':
    driver = open_browser()
    search_field = navigate_to_amazon()
    all_departments = search_for_item(search_field)
    select_department = select_all_department(all_departments)
    select_page_two_button(select_department)
    select_product = select_first_product_of_page_two()
    item_price, quantity = get_price_and_qty(select_product)
    product_title = get_product_title()
    add_product_to_cart()
    select_cart_button()
    subtotal = get_subtotal_amount()
    item_title_in_cart = get_product_title_in_cart()
    if assert_items(product_title, item_title_in_cart):
        if assert_prices(item_price, quantity, subtotal):
            print("Everything it's ok")
    driver.close()
