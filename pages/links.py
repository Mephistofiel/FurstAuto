import difflib
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LinksPage(BasePage):
    def __init__(self, browser, json_file, url=None):
        super().__init__(browser, url)
        self.json_data = self.load_json(json_file)

    def check_links_by_id(self, content_id):
        """Проверяет ссылки на странице, соответствующие заданному ID контента."""
        contents = self.get_content_by_id(content_id)

        for item in contents:
            if item.get('type') != 'link':
                continue  # Пропускаем элементы с другим типом

            selector_info = item['selector']
            selector_type = selector_info.get('type')
            selector_value = selector_info.get('value')
            expected_link = item.get('expected')

            if not isinstance(selector_value, str):
                raise TypeError(f"Значение селектора должно быть строкой, получено: {type(selector_value)}")

            # Выбираем метод поиска в зависимости от типа селектора
            if selector_type == 'css':
                elements = self.find_elements(By.CSS_SELECTOR, selector_value)
            elif selector_type == 'xpath':
                elements = self.find_elements(By.XPATH, selector_value)
            else:
                raise ValueError(f"Неизвестный тип селектора: {selector_type}")

            if not elements:
                allure.attach(
                    f"Элемент с селектором '{selector_value}' не найден.",
                    name="Элемент не найден",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(f"Элемент с селектором '{selector_value}' не найден.")

            # Сбрасываем expected_index для каждого нового селектора
            expected_index = 0

            for element in elements:
                actual_link = element.get_attribute('href')

                if isinstance(expected_link, list):
                    if expected_index < len(expected_link):
                        current_expected_link = expected_link[expected_index]
                    else:
                        raise IndexError(
                            f"Недостаточно ожидаемых ссылок для элементов с селектором '{selector_value}'"
                        )
                else:
                    current_expected_link = expected_link

                self.step_check_link_step(
                    f"{selector_value}[{expected_index}]",
                    actual_link,
                    current_expected_link
                )

                expected_index += 1

    @allure.step("Проверка ссылки для элемента '{selector}'")
    def step_check_link_step(self, selector, actual_link, expected_link):
        """Шаг проверки ссылки элемента."""
        allure.attach(actual_link, name="Фактическая ссылка", attachment_type=allure.attachment_type.TEXT)
        allure.attach(expected_link, name="Ожидаемая ссылка", attachment_type=allure.attachment_type.TEXT)
        if actual_link != expected_link:
            diff = '\n'.join(difflib.ndiff([expected_link], [actual_link]))
            allure.attach(diff, name="Отличия", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"Ссылка не совпадает для элемента '{selector}'.")
