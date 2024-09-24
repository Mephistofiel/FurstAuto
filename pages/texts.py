import difflib
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TextsPage(BasePage):
    def __init__(self, browser, json_file, url=None):
        super().__init__(browser, url)
        self.json_data = self.load_json(json_file)

    def check_texts_by_id(self, content_id):
        """Проверяет тексты на странице, соответствующие заданному ID контента."""
        contents = self.get_content_by_id(content_id)

        for item in contents:
            if item.get('type') != 'text':
                continue  # Пропускаем элементы с другим типом

            selector_info = item['selector']
            selector_type = selector_info.get('type')
            selector_value = selector_info.get('value')
            expected_text = item.get('expected')

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
                actual_text = self.normalize_text(
                    element.get_attribute('innerText').replace('<br>', '\n')
                )

                if isinstance(expected_text, list):
                    if expected_index < len(expected_text):
                        current_expected_text = expected_text[expected_index]
                    else:
                        raise IndexError(
                            f"Недостаточно ожидаемых текстов для элементов с селектором '{selector_value}'"
                        )
                else:
                    current_expected_text = expected_text

                self.step_check_text_step(
                    f"{selector_value}[{expected_index}]",
                    actual_text,
                    current_expected_text
                )

                expected_index += 1

    @allure.step("Проверка текста для элемента '{expected_text}'")
    def step_check_text_step(self, selector, actual_text, expected_text):
        """Шаг проверки текста элемента."""
        allure.attach(actual_text, name="Фактический текст", attachment_type=allure.attachment_type.TEXT)
        allure.attach(expected_text, name="Ожидаемый текст", attachment_type=allure.attachment_type.TEXT)
        if actual_text != expected_text:
            diff = '\n'.join(difflib.ndiff([expected_text], [actual_text]))
            allure.attach(diff, name="Отличия", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"Текст не совпадает для элемента '{expected_text}'.")
