from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class WaitHelpers:

    header_logo = (By.CLASS_NAME, "logo")
    order_modal_body = (By.CSS_SELECTOR, "div.order-body")

    def __init__(self, driver):
        self.driver = driver

    #Espera a que se cargue la seleccion de tarifa/vehiculo
    def wait_for_header_logo(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.header_logo))

    #Espera que se cargue la info del conductor
    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(self.order_modal_body, "El conductor llegará en"))