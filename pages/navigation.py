import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

class NavigationPage(BasePage):
    def __init__(self, browser, json_file, url=None):
        super().__init__(browser, url)
        self.json_data = self.load_json(json_file)


    def get_content_by_id(self, content_id):
        """Извлекает контент из JSON по заданному ID."""
        # Предполагается, что content_id соответствует ключам в JSON
        # Например, "MB.system.frozen_account.ru"
        keys = content_id.split(".")
        data = self.json_data
        for key in keys:
            data = data.get(key, {})
        return data.get('content', [])

    def navigate_links_by_id(self, content_id):
        """Переходит по ссылкам, указанным в JSON для заданного content_id."""
        contents = self.get_content_by_id(content_id)

        for item in contents:
            if item.get('type') != 'link':
                continue  # Пропускаем элементы не являющиеся ссылками

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

            # Приводим expected_link к списку
            if isinstance(expected_link, str):
                expected_links = [expected_link]
            elif isinstance(expected_link, list):
                expected_links = expected_link
            else:
                raise TypeError(f"Поле 'expected' должно быть строкой или списком, получено: {type(expected_link)}")

            if len(expected_links) != len(elements):
                raise AssertionError(
                    f"Количество ожидаемых ссылок ({len(expected_links)}) не совпадает с количеством найденных элементов ({len(elements)})."
                )

            for index, element in enumerate(elements):
                expected_url = expected_links[index]
                actual_href = element.get_attribute('href')

                if not actual_href:
                    raise AssertionError(f"Ссылка отсутствует в элементе '{selector_value}'")

                if actual_href.startswith('mailto:'):
                    # Проверяем только наличие корректного href для mailto-ссылок
                    if actual_href != expected_url:
                        raise AssertionError(f"Фактическая ссылка '{actual_href}' не соответствует ожидаемой '{expected_url}'.")
                    continue  # Пропускаем навигацию по mailto ссылкам

                self.navigate_and_check(element, expected_url)

    @allure.step("Переход по ссылке из элемента и проверка загрузки страницы")
    def step_navigate_and_check(self, element, expected_url):
        """Кликает по ссылке, проверяет загрузку страницы и отсутствие ошибок."""
        original_window = self.browser.current_window_handle
        opened_new_window = False

        try:
            # Ожидаем, что элемент будет кликабельным, затем кликаем
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(element))
            element.click()

            # Проверяем, открылось ли новое окно или вкладка
            WebDriverWait(self.browser, 5).until(
                lambda driver: len(driver.window_handles) > 1
            )
            if len(self.browser.window_handles) > 1:
                new_window = [window for window in self.browser.window_handles if window != original_window][0]
                self.browser.switch_to.window(new_window)
                opened_new_window = True
            else:
                # Ссылка открылась в том же окне
                pass

            # Ожидаем загрузки новой страницы
            self.wait_for_page_load()

            # Получаем фактический URL после перехода
            actual_url = self.browser.current_url

            # Делаем скриншот страницы
            self.attach_screenshot(name="Скриншот страницы")

            # Проверяем, что фактический URL соответствует ожидаемому
            if expected_url and actual_url != expected_url:
                allure.attach(actual_url, name="Фактический URL", attachment_type=allure.attachment_type.TEXT)
                allure.attach(expected_url, name="Ожидаемый URL", attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Фактический URL '{actual_url}' не соответствует ожидаемому '{expected_url}'.")

            # Проверяем отсутствие ошибок на странице
            self.check_no_errors_on_page()

        except TimeoutException:
            allure.attach(self.browser.get_screenshot_as_png(), name="Скриншот ошибки", attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Страница не загрузилась за отведенное время.")

        finally:
            # Закрываем новое окно и возвращаемся к исходному
            if opened_new_window:
                self.browser.close()
                self.browser.switch_to.window(original_window)

    def wait_for_page_load(self, timeout=10):
        """Ожидает полной загрузки страницы."""
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

    def check_no_errors_on_page(self):
        """Проверяет отсутствие ошибок на странице по наличию определенных слов."""
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text.lower()
        error_indicators = ['404', 'not found', '500', 'error']
        if any(error in body_text for error in error_indicators):
            self.attach_screenshot(name="Скриншот ошибки на странице")
            raise AssertionError("На странице обнаружена ошибка.")
