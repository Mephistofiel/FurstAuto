import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'C:/Users/user/PycharmProjects/FurstAuto/pages')))

import pytest
from pages.text import TextPage

@pytest.mark.text
def test_text(browser):
    # Создаем объект TextsPage и передаем путь к JSON
    page = TextPage(browser, json_file='C:/Users/user/PyCharmProjects/FurstAuto/texts.json',
                url='file:///C:/HTML/Mostbet/(MB)%20frozen_account_RU.html')

    page.open_page()

    # Проверяем тексты по ID
    page.check_texts_by_id('1')  # Проверка русского текста
