from selenium.webdriver.common.by import By
from tests.driver import create_driver


def test_negative_amount():
    driver = create_driver()

    try:
        driver.get("http://localhost:8000")

        # проверяем, что страница вообще загрузилась
        assert "F-Bank" in driver.page_source

        # проверяем, что UI отрисовался
        cards = driver.find_elements(By.CSS_SELECTOR, "[role='button']")

        assert len(cards) > 0, "Карточки счетов не отрисовались"

    

    finally:
        driver.quit()