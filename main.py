import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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

    #Espera a que se cargue la seleccion de tarifa/vehiculo
    def wait_for_header_logo(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.header_logo))

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
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.agregar_button)).click()
        self.driver.find_element(*self.close_button).click()
        return self.get_payment()

    def get_message(self):
        return self.driver.find_element(*self.driver_message).get_property('value')

    def send_message_to_driver(self, driver_message):
        self.driver.find_element(*self.driver_message).send_keys(driver_message)
        return self.get_message()

    def toggle_blanket_switch(self):
        # 1. Hacer scroll hasta el contenedor del switch
        container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.blanket_switch_container))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
        time.sleep(1)  # Pequeña pausa para que termine el scroll
        #Localizar el input real (checkbox) que está oculto
        switch_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.blanket_switch_input))
        #Localizar el slider
        switch_slider = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.blanket_switch_slider))
        #Hacer click en el slider
        switch_slider.click()
        return switch_input.is_selected()

    def add_ice_cream(self):
        #Localizar el botón +
        plus_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_plus_button))
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
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.order_modal_body))
        order_body = self.driver.find_element(*self.order_modal_body).text
        return order_body

    #Espera que se cargue la info del conductor
    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(self.order_modal_body, "El conductor llegará en"))

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        # ESTE METODO FUNCIONA PARA SELENIUM >= 4.6

        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test1_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_header_logo()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test2_select_tarifa_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort()
        assert routes_page.is_comfort_tariff_selected()

    def test3_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        number_phone = data.phone_number
        displayed_phone = routes_page.input_phone_number(number_phone)
        assert number_phone in displayed_phone

    def test4_add_credit_card(self ):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        card_code = data.card_code
        displayed_card = routes_page.add_credit_card(card_number, card_code)
        assert "Tarjeta" in displayed_card

    def test5_message_from_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        message_from_driver = data.message_for_driver
        displayed_message = routes_page.send_message_to_driver(message_from_driver)
        assert message_from_driver in displayed_message

    def test6_blanket_switch(self):
        routes_page = UrbanRoutesPage(self.driver)
        # Obtener estado inicial del switch
        initial_state = routes_page.driver.find_element(*routes_page.blanket_switch_input).is_selected()
        # Cambiar el estado del switch
        new_state = routes_page.toggle_blanket_switch()
        # Verificar que el estado cambió
        assert new_state != initial_state, f"El estado del switch debería haber cambiado de {initial_state} a {not initial_state}"

    def test7_add_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        ice_cream_count = routes_page.add_ice_cream()
        assert ice_cream_count == 2, f"Se esperaban 2 helados, pero el contador muestra {ice_cream_count}"

    def test8_order_taxi_modal(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_call_taxi_button()
        modal_title = routes_page.get_order_modal_text()
        assert "Buscar automóvil" in modal_title

    def test9_driver_info_modal(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_driver_info()
        modal_driver = routes_page.get_order_modal_text()
        assert "El conductor llegará en" in modal_driver

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
