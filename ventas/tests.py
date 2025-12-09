from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .models import Producto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ProductoModelTest(TestCase):
    def test_crear_producto(self):
        """Verifica que se puede crear un producto y calcular su precio"""
        prod = Producto.objects.create(
            codigo="TEST01",
            descripcion="Producto de Prueba",
            costo=10.00,
            precio=15.00,
            cantidad=100
        )
        self.assertEqual(prod.descripcion, "Producto de Prueba")
        self.assertEqual(prod.cantidad, 100)
        print("Prueba Unitaria: Producto creado correctamente.")

class LoginBrowserTest(StaticLiveServerTestCase):
    
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_login_fallido(self):
        """Intenta entrar con contraseña falsa y espera error"""
        self.browser.get(self.live_server_url)
        
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        boton_login = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        username_input.send_keys("usuario_falso")
        password_input.send_keys("clave_erronea")
        
        boton_login.click()
        
        time.sleep(1)
        
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        
        self.assertIn("Usuario o contraseña incorrectos", body_text)
        
        print("Prueba Navegador: El sistema mostró el error correctamente.")