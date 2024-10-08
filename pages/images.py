import difflib
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ImagesPage(BasePage):
    def __init__(self, browser, json_file, url=None):
        super().__init__(browser, url)
        self.json_data = self.load_json(json_file)

    def check_images_by_id(self, content_id):
        """Проверяет изображения на странице, соответствующие заданному ID контента."""
        contents = self.get_content_by_id(content_id)

        for item in contents:
            if item.get('type') != 'image':
                continue  # Пропускаем элементы с другим типом

            selector_info = item['selector']
            selector_type = selector_info.get('type')
            selector_value = selector_info.get('value')
            expected_src = item.get('expected')

            if not isinstance(selector_value, str):
                raise TypeError(f"Значение селектора должно быть строкой, получено: {type(selector_value)}")

            # Выбор метода поиска в зависимости от типа селектора
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

            expected_index = 0

            for element in elements:
                actual_src = element.get_attribute('src')

                if isinstance(expected_src, list):
                    if expected_index < len(expected_src):
                        current_expected_src = expected_src[expected_index]
                    else:
                        raise IndexError(
                            f"Недостаточно ожидаемых src для элементов с селектором '{selector_value}'"
                        )
                else:
                    current_expected_src = expected_src

                self.check_image_step(
                    f"{selector_value}[{expected_index}]",
                    actual_src,
                    current_expected_src,
                    element  # передаем элемент изображения
                )

                expected_index += 1

    @allure.step("Проверка src для изображения '{selector}'")
    def check_image_step(self, selector, actual_src, expected_src, element):
        """Шаг проверки src изображения."""
        allure.attach(actual_src, name="Фактический src", attachment_type=allure.attachment_type.TEXT)
        allure.attach(expected_src, name="Ожидаемый src", attachment_type=allure.attachment_type.TEXT)

        # Делаем скриншот элемента изображения
        image_screenshot = element.screenshot_as_png
        allure.attach(image_screenshot, name="Скриншот изображения", attachment_type=allure.attachment_type.PNG)

        if actual_src != expected_src:
            diff = '\n'.join(difflib.ndiff([expected_src], [actual_src]))
            allure.attach(diff, name="Отличия", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"src изображения не совпадает для элемента '{selector}'.")

