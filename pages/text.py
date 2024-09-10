import re
from selenium.webdriver.common.by import By
from base_page import BasePage
import json
import difflib


class TextPage(BasePage):
    def __init__(self, browser, json_file, url=None):
        super().__init__(browser, url)
        self.json_data = self.load_json(json_file)
        self.text_selectors = [
            'a[href="https://mostbet-ru30.com/profile/refill?utm_medium=email&utm_source=system&content=refill&utm_campaign=frozen_account"] > span',
            'a[href="https://mostbet-ru30.com/pregame?utm_medium=email&utm_source=system&content=pregame&utm_campaign=frozen_account"]',
            'a[href="https://mostbet-ru30.com/live?utm_medium=email&utm_source=system&content=live&utm_campaign=frozen_account"]',
            'a[href="https://mostbet-ru30.com/casino?utm_medium=email&utm_source=system&content=casino&utm_campaign=frozen_account"]',
            'a[href="https://mostbet-ru30.com/live-casino?utm_medium=email&utm_source=system&content=live_casino&utm_campaign=frozen_account"]',
            'a[href="https://mostbet-ru30.com/aviator?utm_medium=email&utm_source=system&content=aviator&utm_campaign=frozen_account"]',
            'a[href="https://mostbet-ru30.com/profile/edit?utm_medium=email&utm_source=system&content=button1&utm_campaign=frozen_account"]',
            'span span span[style="background: #001d3a; color: #ffffff; mix-blend-mode: difference"]',
            'a[href="mailto:id@mostbet.com"]',
            'a[href="mailto:support@mostbet.com"] > span > span',
            'a[href = "#UNSUBSCRIBE_HREF#"] > span > span'
        ]

    def normalize_text(self, text):
        """Очищает текст от лишних пробелов и форматирует переносы."""
        return re.sub(r'\n+', '\n', re.sub(r'\s+', ' ', text).strip())

    def load_json(self, json_file):
        """Загружает данные из JSON файла."""
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_text_by_id(self, text_id):
        """Получает текст по ID из JSON."""
        for section, data in self.json_data['MB']['system']['frozen_account'].items():
            if data['id'] == text_id:
                return data['text']
        raise ValueError(f"Текст для ID {text_id} не найден")

    def check_texts_by_id(self, text_id):
        """Сравнивает тексты на странице с текстами из JSON по ID."""
        expected_texts = self.get_text_by_id(text_id)
        expected_index = 0

        for selector in self.text_selectors:
            elements = self.find_elements(By.CSS_SELECTOR, selector)

            for element in elements:
                element_text = self.normalize_text(element.get_attribute('innerHTML').replace('<br>', '\n'))

                print(
                    f"Сравнение текста для селектора {selector}: Ожидаемый: '{expected_texts[expected_index]}', Полученный: '{element_text}'")

                if element_text != expected_texts[expected_index]:
                    diff = '\n'.join(difflib.ndiff(expected_texts[expected_index], element_text))
                    raise AssertionError(f"Текст не совпадает. Отличия:\n{diff}")

                expected_index += 1
