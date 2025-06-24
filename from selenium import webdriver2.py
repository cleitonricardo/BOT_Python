from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import json
import requests

# Configurações iniciais
URL_BASE = "https://autooleoapp.com.br/app/veiculo.html?id="
LOGIN_URL = "https://autooleoapp.com.br/app/login.html"
POST_URL = "https://7kkxcxqz-5000.brs.devtunnels.ms/register/veiculo"
EMAIL = "Limagarcia1305@gmail.com"
SENHA = "015006"

def limitar_str(texto, limite=255):
    if not texto:
        return ""
    return str(texto).strip()[:limite]

def setup_driver():
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)

def login(driver):
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(EMAIL)
    driver.find_element(By.ID, 'senha').send_keys(SENHA)
    driver.find_element(By.ID, 'botaoEnviar').click()
    WebDriverWait(driver, 10).until(EC.url_changes(LOGIN_URL))

def extrair_lista(soup, class_name):
    lista = []
    divs = soup.find_all('div', class_='card listaDados ' + class_name)
    for item in divs:
        texto = item.text.strip().replace('ads_click', '').strip()
        if texto:
            lista.append(texto)
    return lista

def juntar_pares(lista):
    pares = []
    for i in range(0, len(lista), 2):
        if i + 1 < len(lista):
            pares.append(f"{lista[i]} {lista[i+1]}")
        else:
            pares.append(lista[i])
    return ', '.join(pares)

def processar_veiculo(driver, id_veiculo):
    driver.get(URL_BASE + str(id_veiculo))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    modelo = driver.find_element(By.CLASS_NAME, 'modelo').text.replace('\n', ' ').strip()
    print(f'"Modelo": "{modelo}"')

    ano_match = re.search(r'(\d{4})\s+ATÉ\s+(\d{4})', modelo)
    anos = ', '.join([str(ano) for ano in range(int(ano_match.group(1)), int(ano_match.group(2)) + 1)]) if ano_match else "Não encontrado"

    # Monta dicionário com os dados extraídos, limitando tamanho de cada campo
    dados = {
        "Marca": limitar_str(" "),
        "Modelo": limitar_str(modelo),
        "Ano": limitar_str(anos),
        "OleoMotor": limitar_str(', '.join(extrair_lista(soup, 'marcas_1'))),
        "QuantidadeOleoMotor": limitar_str(driver.find_element(By.CLASS_NAME, 'card').find_element(By.TAG_NAME, 'p').text.replace('Litros', '').strip()),
        "FiltroOleo": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_11'))),
        "FiltroArMotor": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_12'))),
        "PalhetaLimpadorDianteira": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_44'))),
        "FiltroCombustivel": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_13'))),
        "FiltroCabine": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_14'))),
        "FluidoCambioAutomatico": limitar_str(', '.join(extrair_lista(soup, 'marcas_2') + extrair_lista(soup, 'marcas_137'))),
        "QuantidadeFluidoCambioAutomatico": limitar_str(" "),
        "FiltroCambioAutomatico": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_15'))),
        "FluidoCambioManual": limitar_str(', '.join(extrair_lista(soup, 'marcas_3'))),
        "QuantidadeFluidoCambioManual": limitar_str(" "),
        "OleoDiferencialTraseiro": limitar_str(', '.join(extrair_lista(soup, 'marcas_7'))),
        "QuantidadeOleoDiferencialTraseiro": limitar_str(" "),
        "AditivoRadiador": limitar_str(juntar_pares(extrair_lista(soup, 'marcas_26'))),
        "QuantidadeAditivoRadiador": limitar_str(" "),
        "FluidoFreio": limitar_str(', '.join(extrair_lista(soup, 'marcas_10'))),
        "QuantidadeFluidoFreio": limitar_str("1,0"),
        "FluidoDirecao": limitar_str(', '.join(extrair_lista(soup, 'marcas_9') + extrair_lista(soup, 'marcas_78'))),
        "QuantidadeFluidoDirecao": limitar_str("1,0")
    }

    return dados

def enviar_dados(dados):
    response = requests.post(POST_URL, headers={"Content-Type": "application/json"}, data=json.dumps(dados, ensure_ascii=False))
    if response.status_code in [200, 201]:
        print("✅ Dados enviados com sucesso!")
    else:
        print(f"❌ Erro ao enviar dados: {response.status_code}")
        print(response.text)

# Execução
if __name__ == "__main__":
    for i in range(2604, 2605):  # Altere o range conforme necessário
        time.sleep(5)
        driver = setup_driver()
        try:
            login(driver)
            dados = processar_veiculo(driver, i)
            print(json.dumps(dados, indent=4, ensure_ascii=False))
            enviar_dados(dados)
        except Exception as e:
            print(f"Erro ao processar veículo {i}: {e}")
        finally:
            driver.quit()
