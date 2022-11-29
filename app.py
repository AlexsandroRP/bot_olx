from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument) # passar os argumentos pro chrome options


    chrome_options.add_experimental_option('prefs', {
        # Desabilitar a confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,

    })

    # inicializando o webdriver e atualizando automaticamente de acordo com a versão do chrome do pc
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    
    return driver
produto = input("Qual produto deseja monitor? ")

# Navegar até um site
driver = iniciar_driver()
driver.get(f'https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul?q={produto}')
while True:
    sleep(5)

    # Carregar todos os elementos da tela movento o scroll
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(2)

    # Encontrar os titulos
    titulos = driver.find_elements(By. XPATH, "//div[@class='sc-12rk7z2-7 kDVQFY']//h2")

    # Encontrar os preços
    precos = driver.find_elements(By. XPATH, "//span[@class='m7nrfa-0 eJCbzj sc-ifAKCX jViSDP']")

    # Encontrar os links
    links = driver.find_elements(By.XPATH, "//a[@data-lurker-detail='list_id']")

    # Guardar isso em um arquivo .csv
    for titulo, preco, link in zip(titulos, precos, links):
        with open('precos.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};{preco.text};{link_processado}{os.linesep}')

    # Fazer isso para todas as páginas existente
    try:
        botao = driver.find_element(By. XPATH, "//span[text()='Próxima pagina']")
        sleep(2)
        botao.click()
    except:
        print("Chegamos na ultima página")
        break    

input('')
driver.close()
