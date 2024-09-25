import allure
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'C:/Users/user/PycharmProjects/FurstAuto/pages')))

import pytest
from pages.texts import TextsPage
from pages.links import LinksPage
from pages.images import ImagesPage
from pages.navigation import NavigationPage

@allure.title("Тест проверки текста")
@pytest.mark.text
def test_text(browser):
    page = TextsPage(browser, json_file='data.json', url='https://Mephistofiel.github.io/HTML/Mostbet/(MB)%20frozen_account_RU.html')
    page.open_page()
    page.check_texts_by_id('1')

@allure.title("Тест проверки ссылок")
@pytest.mark.links
def test_links(browser):
    page = LinksPage(browser, json_file='data.json', url='https://Mephistofiel.github.io/HTML/Mostbet/(MB)%20frozen_account_RU.html')
    page.open_page()
    page.check_links_by_id('1')

@allure.title("Тест проверки изображений")
@pytest.mark.image
def test_images(browser):
    page = ImagesPage(browser, json_file='data.json', url='https://Mephistofiel.github.io/HTML/Mostbet/(MB)%20frozen_account_RU.html')
    page.open_page()
    page.check_images_by_id('1')

@allure.title("Тест проверки перехода на страницы")
@pytest.mark.navigate
def test_navigate(browser):
    page = NavigationPage(browser, json_file='data.json', url='https://Mephistofiel.github.io/HTML/Mostbet/(MB)%20frozen_account_RU.html')
    page.open_page()
    page.navigate_links_by_id('1')