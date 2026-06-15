import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # <-- Добавили импорт

def test_negative_amount_transfer(driver):
    """
    Тест проверяет, что система НЕ позволяет перевести отрицательную сумму.
    Ожидаемое поведение: перевод блокируется.
    Фактическое поведение (БАГ): перевод проходит, появляется алерт об успехе.
    """
    # Открываем страницу с заданным балансом
    driver.get("http://localhost:8000/?balance=30000&reserved=0")
    wait = WebDriverWait(driver, 10)

    # 1. Кликаем на первую карточку счета
    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[role='button']")))
    cards[0].click()
    time.sleep(0.5)

    # 2. Заполняем поле номера карты (16 цифр)
    card_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="0000 0000 0000 0000"]')))
    card_input.send_keys("1234123412341234")
    
    # 3. Вводим отрицательную сумму
    amount_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="1000"]')
    amount_input.clear()
    amount_input.send_keys("-1000")
    time.sleep(0.5)

    # 4. Ищем кнопку Перевести и кликаем
    transfer_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Перевести')]")))
    transfer_btn.click()

    # 5. Ловим алерт
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept() # Закрываем алерт
    except TimeoutException:
        # Если алерт не появился за 10 секунд, тест падает здесь
        raise AssertionError("Тест не смог поймать ожидаемый алерт успеха.")
        
    # 6. Проверка бага 
    assert "принят банком" not in alert_text, \
        f"БАГ НАЙДЕН: Система успешно проводит перевод с отрицательной суммой. Текст алерта: {alert_text}"