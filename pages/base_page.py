class BasePage:
    def __init__(self, browser, url=None):
        self.browser = browser
        self.url = url

    def find_element(self, *args):
        return self.browser.find_element(*args)

    def find_elements(self, *locator):
        return self.browser.find_elements(*locator)

    def open_page(self):
        self.browser.get(self.url)

    def set_url(self, url):
        self.url = url
