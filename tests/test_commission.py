from selenium.webdriver.common.by import By
from tests.driver import create_driver


def test_commission():
    driver = create_driver()

    try:
        driver.get("http://localhost:8000/?balance=30000&reserved=0")

        page = driver.page_source

        # проверяем, что данные баланса реально отображаются
        assert "30" in page or "30000" in page, "Баланс не отображается"

        # проверяем наличие UI карточек
        cards = driver.find_elements(By.CSS_SELECTOR, "[role='button']")

        assert len(cards) >= 3, "Карточки валют не найдены"

    finally:
        driver.quit()