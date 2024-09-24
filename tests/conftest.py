import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture()
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск браузера в headless режиме
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")

    # Укажите путь к вашему chromedriver, если необходимо
    service = ChromeService()

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()