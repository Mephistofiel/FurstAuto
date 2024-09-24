import os
import json
import re
import allure
from utils.decorators import step_with_screenshot, apply_decorator_to_methods

class BasePage(metaclass=apply_decorator_to_methods(step_with_screenshot, method_prefix='step_')):
    def __init__(self, browser, url=None):
        self.browser = browser
        self.url = url

    def open_page(self):
        if self.url:
            self.browser.get(self.url)
        else:
            raise ValueError("URL не задан для страницы.")

    def set_url(self, url):
        self.url = url

    def find_element(self, by, value):
        return self.browser.find_element(by, value)

    def find_elements(self, by, value):
        return self.browser.find_elements(by, value)

    def load_json(self, json_file):
        """Загружает данные из JSON файла."""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        json_file_path = os.path.join(data_dir, json_file)
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_content_by_id(self, content_id):
        """Получает контент по ID из загруженного JSON."""
        data = self.json_data.get('MB', {}).get('system', {}).get('frozen_account', {}).get('ru', {})
        if data.get('id') == content_id:
            return data.get('content', [])
        else:
            raise ValueError(f"Контент для ID {content_id} не найден")

    def attach_screenshot(self, name="Скриншот"):
        """Прикрепляет скриншот к отчету Allure."""
        allure.attach(
            self.browser.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )



    @staticmethod
    def normalize_text(text):
        """Очищает текст от лишних пробелов и форматирует переносы."""
        return re.sub(r'\s+', ' ', text).strip()
