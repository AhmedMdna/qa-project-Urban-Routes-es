from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import time

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    header_logo = (By.CLASS_NAME, "logo")

    taxi_button = (By.CSS_SELECTOR, "button.button.round")
    comfort_icon = (By.CSS_SELECTOR, "div.tcard-icon img[alt='Comfort']")

    phone_field = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    phone_input_text = (By.CSS_SELECTOR, "div.np-text")
    phone_next_button = (By.CLASS_NAME, "button.full")

    sms_code_input = (By.ID, "code")
    sms_send_button =  (By.XPATH, "//button[contains(@class, 'button full') and text()='Confirmar']")

    payment_button = (By.CLASS_NAME, "pp-button.filled")
    add_card_button = (By.CLASS_NAME, "pp-plus-container")
    card_number_field = (By.CSS_SELECTOR, "input#number.card-input")
    card_code_field = (By.CSS_SELECTOR, "input#code.card-input")
    agregar_button = (By.XPATH, "//form[.//input[@id='number']]//button[text()='Agregar']")
    close_button = (By.XPATH, "//div[contains(@class, 'section active')]//div[text()='Método de pago']/preceding-sibling::button")
    text_payment = (By.CLASS_NAME, "pp-value-text")

    driver_message = (By.ID, "comment")

    blanket_switch_container = (By.XPATH, "//div[@class='r-sw-label' and contains(text(), 'Manta y pañuelos')]/parent::div")
    blanket_switch_input = (By.XPATH, "//div[@class='r-sw-label' and contains(text(), 'Manta y pañuelos')]/following-sibling::div//input[@type='checkbox']")
    blanket_switch_slider = (By.XPATH, "//div[contains(@class, 'r-sw-label') and contains(text(), 'Manta y pañuelos')]/following-sibling::div[contains(@class, 'r-sw')]//span[contains(@class, 'slider')]")

    ice_cream_plus_button = (By.XPATH, "//div[contains(@class, 'r-counter-label') and contains(text(), 'Helado')]/following-sibling::div[contains(@class, 'r-counter')]//div[contains(@class, 'counter-plus')]")
    ice_cream_counter = (By.XPATH, "//div[@class='r-counter-label' and contains(text(), 'Helado')]/following-sibling::div[@class='r-counter']//div[@class='counter-value']")

    call_taxi_button = (By.XPATH, "//button[@class='smart-button']")
    order_modal_body = (By.CSS_SELECTOR, "div.order-body")
    #order_header_title = (By.CLASS_NAME, "order-header-title")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def click_tarifa_comfort(self):
        self.driver.find_element(*self.comfort_icon).click()

    def select_comfort(self):
        self.click_taxi_button()
        self.click_tarifa_comfort()

    def is_comfort_tariff_selected(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "div.tcard.active")
        return "Comfort" in element.text

    def get_phone(self):
        return self.driver.find_element(*self.phone_input_text).text

    def input_phone_number(self, number_phone):
        self.driver.find_element(*self.phone_field).click()
        self.driver.find_element(*self.phone_input).send_keys(number_phone)
        self.driver.find_element(*self.phone_next_button).click()
        from helpers import retrieve_phone_code
        code_retrieved = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.sms_code_input).send_keys(code_retrieved)
        self.driver.find_element(*self.sms_send_button).click()
        return self.get_phone()

    def get_payment(self):
        return self.driver.find_element(*self.text_payment).text

    def add_credit_card(self, card_number, card_code):
        self.driver.find_element(*self.payment_button).click()
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        self.driver.find_element(*self.card_code_field).send_keys(card_code)
        #Presionar TAB para cambiar foco
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)
        #Esperar a que el botón se active
        wait = WebDriverWait(self.driver, 5)
        agregar_button_element = wait.until(EC.element_to_be_clickable(self.agregar_button))
        agregar_button_element.click()
        self.driver.find_element(*self.close_button).click()
        return self.get_payment()

    def get_message(self):
        return self.driver.find_element(*self.driver_message).get_property('value')

    def send_message_to_driver(self, driver_message):
        self.driver.find_element(*self.driver_message).send_keys(driver_message)
        return self.get_message()

    def toggle_blanket_switch(self):
        # 1. Hacer scroll hasta el contenedor del switch
        wait = WebDriverWait(self.driver, 10)
        container = wait.until(EC.presence_of_element_located(self.blanket_switch_container))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
        time.sleep(1)  # Pequeña pausa para que termine el scroll
        #Localizar el input real (checkbox) que está oculto
        switch_input = wait.until(EC.presence_of_element_located(self.blanket_switch_input))
        #Localizar el slider
        switch_slider = wait.until(EC.element_to_be_clickable(self.blanket_switch_slider))
        #Hacer click en el slider
        switch_slider.click()
        return switch_input.is_selected()

    def add_ice_cream(self):
        #Localizar el botón +
        wait = WebDriverWait(self.driver, 10)
        plus_button = wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        #Hacer scroll
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", plus_button)
        time.sleep(1)  # Pequeña pausa para que termine el scroll
        #Hacer click 2 veces
        plus_button.click()
        time.sleep(0.3)  # Pequeña pausa entre clicks
        plus_button.click()

        value = self.driver.find_element(*self.ice_cream_counter).text
        return int(value)

    def click_call_taxi_button(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def get_order_modal_text(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.order_modal_body))
        order_body = self.driver.find_element(*self.order_modal_body).text
        return order_body