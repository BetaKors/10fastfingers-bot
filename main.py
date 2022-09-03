from operator import attrgetter
from typing import Iterator
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as IsElementClickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class TypingBot:
    def __init__(self) -> None:
        self._driver = self._get_driver()
        self._url = 'https://10fastfingers.com/typing-test/portuguese/'

        self._cookie_xpath = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
        self._word_list_xpath = '//*[@id="row1"]'
        self._first_word_xpath = self._word_list_xpath + '/span[1]'

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._driver.quit()

    def begin(self) -> None:
        self._driver.get(self._url)

        self._handle_cookie_policy()

        self._wait_until_element(self._first_word_xpath)

        # stop page from loading so that a video ad doesn't load and break everything.
        # this may not always work, since apparently the video may load before the first word
        # on the list of words.
        # also sometimes it loads but doesn't break anything ¯\_(ツ)_/¯
        self._driver.execute_script('window.stop();')

        self._type_words()

        while self._is_window_open():
            pass

    def _handle_cookie_policy(self) -> None:
        self._wait_until_element(self._cookie_xpath)
        self._click_element(self._cookie_xpath)

    def _type_words(self) -> None:
        input_field = self._find_by_xpath('//*[@id="inputfield"]')

        for word in self._get_words():
            self._enter_word(input_field, word)

    def _get_words(self) -> Iterator[str]:
        words_list_div = self._find_by_xpath(self._word_list_xpath)
        children = words_list_div.find_elements(By.CSS_SELECTOR, '*')
        return map(attrgetter('text'), children)

    def _enter_word(self, input_field: WebElement, word: WebElement) -> None:
        input_field.send_keys(word + ' ')

    def _wait_until_element(self, xpath: str) -> None:
        locator = By.XPATH, xpath
        element_is_clickable = IsElementClickable(locator)

        wait = WebDriverWait(self._driver, timeout=10)

        wait.until(element_is_clickable)

    def _find_by_xpath(self, xpath: str) -> WebElement:
        return self._driver.find_element(By.XPATH, xpath)

    def _click_element(self, xpath: str) -> None:
        self._find_by_xpath(xpath).click()

    def _is_window_open(self) -> bool:
        return self._driver.window_handles

    def _get_driver(self) -> Chrome:
        service = Service(
            ChromeDriverManager().install()
        )

        options = Options()
        options.add_argument('start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        return Chrome(
            service=service,
            options=options
        )


with TypingBot() as bot:
    bot.begin()
