import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from UrbanRoutesPage import UrbanRoutesPage
from WaitHelpers import WaitHelpers

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        # ESTE METODO FUNCIONA PARA SELENIUM >= 4.6

        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.wait_helpers = WaitHelpers(cls.driver)

    def test1_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.wait_helpers.wait_for_header_logo()
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
        self.wait_helpers.wait_for_driver_info()
        modal_driver = routes_page.get_order_modal_text()
        assert "El conductor llegará en" in modal_driver

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()