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

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

OleoMotor = []
FiltroOleo = []
FiltroArMotor = []
PalhetaLimpadorDianteira = []
FiltroCombustivel = []
FiltroCabine = []
FluidoCambioAutomatico = []
FiltroCambioAutomatico = []
FluidoCambioManual = []
OleoDiferencialTraseiro = []
OleoDiferencialDianteiro = []
AditivoRadiador = []
FluidoFreio = []
FluidoDirecao = []
# Abra a tela de login
driver.get("https://autooleoapp.com.br/app/login.html")

try:
    # Espera até que o campo de login apareça
    login_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))  # Ajuste o seletor
    )
    password_field = driver.find_element(By.ID, 'senha')  # Ajuste o seletor
    login_button = driver.find_element(By.ID, 'botaoEnviar')  # Ajuste o seletor

    # Preenche as credenciais
    login_field.send_keys('Limagarcia1305@gmail.com')  # Substitua pelo login
    password_field.send_keys('015006')  # Substitua pela senha

    # Clica no botão de login
    login_button.click()

    # Aguarda até que a página principal carregue
    WebDriverWait(driver, 10).until(
        EC.url_changes("https://autooleoapp.com.br/app/login.html")
    )



    # Acessa a página desejada
    driver.get("https://autooleoapp.com.br/app/veiculo.html?id=58")
    
    # Espera até que os elementos estejam carregados
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card'))
    )
    
    # Captura o HTML da página atual
    page_html = driver.page_source

    # Usa o BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(page_html, 'html.parser')

    


    # Alternativa usando Selenium diretamente


    veiculo_nome_selenium = driver.find_element(By.CLASS_NAME, 'modelo').text
    veiculo_nome_selenium_linha_unica = veiculo_nome_selenium.replace('\n', ' ').strip()

    # Exibe o modelo na mesma linha
    print('"Modelo"', ':', '"', veiculo_nome_selenium_linha_unica, '",')



    ano_match = re.search(r'(\d{4})\s+ATÉ\s+(\d{4})', veiculo_nome_selenium)

    if ano_match:
        # Extrai os anos de acordo com o padrão encontrado
        ano_inicio = int(ano_match.group(1))
        ano_fim = int(ano_match.group(2))

        # Gera uma lista de anos sequenciais
        anos_sequenciais = [str(ano) for ano in range(ano_inicio, ano_fim + 1)]

        # Converte a lista de anos em uma string separada por vírgulas
        anos_sequenciais_str = ', '.join(anos_sequenciais)

        # Exibe os anos sequenciais
        print('"Ano"', ':', '"', anos_sequenciais_str, '",')
    else:
        print("Ano não encontrado no texto.")



    # Captura os dados da lista de marcas de óleo

    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_1')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip() # Remove espaços extras
            OleoMotor.append(item_texts)
    # Captura mais marcas na seção de sugestões, ignorando 'ads_click'
    marcas_oleo_str = ', '.join(OleoMotor)

# Exibe a string resultante
    print('"OleoMotor"',':','"',marcas_oleo_str,'",')

    # Captura o texto da quantidade de óleo
    litros_text_selenium = driver.find_element(By.CLASS_NAME, 'card').find_element(By.TAG_NAME, 'p').text

    # Remove a palavra "Litros" do texto
    litros_text_selenium = litros_text_selenium.replace('Litros', '').strip()

    # Exibe o texto sem a palavra "Litros"
    print('"QuantidadeOleoMotor"', ':', '"', litros_text_selenium, '",')



    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_11')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FiltroOleo.append(item_texts)

        if FiltroOleo:
    # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FiltroOleo)
            elementos = filtro_oleo_str.split(", ")
            resultado_filtro_oleo_str = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
            # Exibe a string resultante
            print('"FiltroOleo"',':','"',resultado_filtro_oleo_str,'",')

        else:
            print('"FiltroCombustivel"', ':', '"",')

    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_12')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FiltroArMotor.append(item_texts)

        if FiltroArMotor:
            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FiltroArMotor)
            elementos = filtro_oleo_str.split(", ")
            resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
            # Exibe a string resultante
            print('"FiltroArMotor"',':','"',resultado,'",')

        else:
            print('"FiltroArMotor"', ':', '"",')




    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_44')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            PalhetaLimpadorDianteira.append(item_texts)
        if PalhetaLimpadorDianteira:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(PalhetaLimpadorDianteira)
            elementos = filtro_oleo_str.split(", ")
            resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
            # Exibe a string resultante
            print('"PalhetaLimpadorDianteira"',':','"',resultado,'",')

        else:
            print('"PalhetaLimpadorDianteira"', ':', '"",')





    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_13')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FiltroCombustivel.append(item_texts)



    if FiltroCombustivel:
        # Converte a lista de filtros de óleo em uma string separada por vírgula
        filtro_oleo_str = ', '.join(FiltroCombustivel)
        elementos = filtro_oleo_str.split(", ")
        resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
        # Exibe a string resultante
        print('"FiltroCombustivel"',':','"',resultado,'",')

    else:
        print('"FiltroCombustivel"', ':', '"",')
       



    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_14')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FiltroCabine.append(item_texts)

        if FiltroCabine:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FiltroCabine)

            elementos = filtro_oleo_str.split(", ")
            resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])


            # Exibe a string resultante
            print('"FiltroCabine"',':','"',resultado,'",')

        else:
            print('"FiltroCabine"', ':', '"",')



    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_2')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoCambioAutomatico.append(item_texts)

        if FluidoCambioAutomatico:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoCambioAutomatico)

            # Exibe a string resultante
            print('"FluidoCambioAutomatico"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoCambioAutomatico"',':','"','",')

        else:
            print('"FluidoCambioAutomatico"', ':', '"",')
            print('"QuantidadeFluidoCambioAutomatico"',':','"','",')


    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_137')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoCambioAutomatico.append(item_texts)

        if FluidoCambioAutomatico:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoCambioAutomatico)

            # Exibe a string resultante
            print('"FluidoCambioAutomatico"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoCambioAutomatico"',':','"','",')

        else:
            print('"FluidoCambioAutomatico"', ':', '"",')
            print('"QuantidadeFluidoCambioAutomatico"',':','"','",')




    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_15')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FiltroCambioAutomatico.append(item_texts)

        if FiltroCambioAutomatico:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FiltroCambioAutomatico)
            elementos = filtro_oleo_str.split(", ")
            resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
            # Exibe a string resultante
            print('"FiltroCambioAutomatico"',':','"',resultado,'",')
            

        else:
            print('"FiltroCambioAutomatico"', ':', '"",')




    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_3')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoCambioManual.append(item_texts)

        if FluidoCambioManual:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoCambioManual)

            # Exibe a string resultante
            print('"FluidoCambioManual"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoCambioManual"',':','"','",')
            

        else:
            print('"FiltroCambioAutomatico"', ':', '"",')
            print('"QuantidadeFluidoCambioManual"',':','"','",')



    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_7')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            OleoDiferencialTraseiro.append(item_texts)
        if OleoDiferencialTraseiro:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(OleoDiferencialTraseiro)

            # Exibe a string resultante
            print('"OleoDiferencialTraseiro"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeOleoDiferencialTraseiro"',':','"','",')

        else:
            print('"OleoDiferencialTraseiro"', ':', '"",')
            print('"QuantidadeOleoDiferencialTraseiro"',':','"','",')

   
    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_26')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            AditivoRadiador.append(item_texts)

    # Converte a lista de filtros de óleo em uma string separada por vírgula
    if AditivoRadiador:
        filtro_oleo_str = ', '.join(AditivoRadiador)
        elementos = filtro_oleo_str.split(", ")
        resultado = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
        
        # Exibe a string resultante
        print('"AditivoRadiador"', ':', '"', resultado, '",')
        print('"QuantidadeAditivoRadiador"', ':', '"', '",')
    else:
        print('"AditivoRadiador"', ':', '"",')
        print('"QuantidadeAditivoRadiador"', ':', '"",')
   
   
   
    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_10')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoFreio.append(item_texts)
        if FluidoFreio:

            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoFreio)

            # Exibe a string resultante
            print('"FluidoFreio"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoFreio"',':','"1,0",')

        else:
            print('"OleoDiferencialTraseiro"', ':', '"",')
            print('"QuantidadeFluidoFreio"',':','"','",')            


 
 
 
    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_9')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoDirecao.append(item_texts)
        if FluidoDirecao:
            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoDirecao)

            # Exibe a string resultante
            print('"FluidoDirecao"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoDirecao"',':','"1,0"')
        else:
            print('"FluidoDirecao"', ':', '"",')
 



    lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_78')
    if lista_dados_elementss:
        for items in lista_dados_elementss:
            item_texts = items.text.strip()  # Captura o texto do item e remove espaços extras
            
            # Se o texto contiver 'ads_click', removemos essa parte
            if 'ads_click' in item_texts:
                item_texts = item_texts.replace('ads_click', '').strip()
            
            # Adiciona o filtro de óleo à lista
            FluidoDirecao.append(item_texts)
        if FluidoDirecao:
            # Converte a lista de filtros de óleo em uma string separada por vírgula
            filtro_oleo_str = ', '.join(FluidoDirecao)

            # Exibe a string resultante
            print('"FluidoDirecao"',':','"',filtro_oleo_str,'",')
            print('"QuantidadeFluidoDirecao"',':','"1,0"')

        else:
            print('"FluidoDirecao"', ':', '"",')




except Exception as e:
    print("Erro:", e)

finally:
    # Fecha o navegador
    driver.quit()
