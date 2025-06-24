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

for i in range(2605, 2606):
    time.sleep(5)
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

    output = []

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
            driver.get("https://autooleoapp.com.br/app/veiculo.html?id=" + str(i))
            
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

            output.append(f'"Modelo": "{veiculo_nome_selenium_linha_unica}"')

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
                output.append(f'"Ano": "{anos_sequenciais}"')
            else:
                print("Ano não encontrado no texto.")
                output.append('"Ano": "Não encontrado"')


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
            output.append(f'"OleoMotor": "{", ".join(OleoMotor)}"')
            # Captura o texto da quantidade de óleo
            litros_text_selenium = driver.find_element(By.CLASS_NAME, 'card').find_element(By.TAG_NAME, 'p').text

            # Remove a palavra "Litros" do texto
            litros_text_selenium = litros_text_selenium.replace('Litros', '').strip()
            output.append(f'"QuantidadeOleoMotor": "{litros_text_selenium}"')
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
                    resultado_filtro_oleo_str = ""
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
            else:
                resultado =""


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
                    resultados = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
                    # Exibe a string resultante
                    print('"PalhetaLimpadorDianteira"',':','"',resultados,'",')

                else:
                    print('"PalhetaLimpadorDianteira"', ':', '"",')

            else:
                resultados =""

            lista_dados_elementss = soup.find_all('div', class_='card listaDados marcas_13')
            FiltroCombustivel = []

            if lista_dados_elementss:
                for items in lista_dados_elementss:
                    item_texts = items.text.strip()
                    
                    if 'ads_click' in item_texts:
                        item_texts = item_texts.replace('ads_click', '').strip()
                    
                    FiltroCombustivel.append(item_texts)

            if FiltroCombustivel:
                # Converte a lista em uma string separada por vírgula
                filtro_oleo_str = ', '.join(FiltroCombustivel)
                elementos = filtro_oleo_str.split(", ")

                # Construindo `resultadoss` sem erro de índice
                pares = []
                for i in range(0, len(elementos), 2):
                    if i + 1 < len(elementos):
                        pares.append(f"{elementos[i]} {elementos[i+1]}")
                    else:
                        pares.append(elementos[i])  # Adiciona o último item sem par

                resultadoss = ", ".join(pares)
            else:
                resultadoss = ""

            print('"FiltroCombustivel"', ':', f'"{resultadoss}",')


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
                    resultadosss = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])


                    # Exibe a string resultante
                    print('"FiltroCabine"',':','"',resultadosss,'",')

                else:
                    resultadosss = ""
                    print('"FiltroCabine"', ':', '"",')
            else:
                resultadosss = ""
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
                    filtro_oleo_strs = ', '.join(FluidoCambioAutomatico)[:255]

                    # Exibe a string resultante
                    print('"FluidoCambioAutomatico"',':','"',filtro_oleo_strs,'",')
                    print('"QuantidadeFluidoCambioAutomatico"',':','"','",')

                else:
                    print('"FluidoCambioAutomatico"', ':', '"",')
                    print('"QuantidadeFluidoCambioAutomatico"',':','"','",')
            else:
                filtro_oleo_strs = " "
                print('"FiltroCabine"', ':', '" ",')

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
                    filtro_oleo_strss = ', '.join(FluidoCambioAutomatico)

                    # Exibe a string resultante
                    print('"FluidoCambioAutomatico"',':','"',filtro_oleo_strss,'",')
                    print('"QuantidadeFluidoCambioAutomatico"',':','"','",')

                else:
                    print('"FluidoCambioAutomatico"', ':', '"",')
                    print('"QuantidadeFluidoCambioAutomatico"',':','"','",')
            else:
                filtro_oleo_strss =" "
                print('"FluidoCambioAutomatico"', ':', '" ",')



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
                    resultadossss = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
                    # Exibe a string resultante
                    print('"FiltroCambioAutomatico"',':','"',resultadossss,'",')
                    

                else:
                    print('"FiltroCambioAutomatico"', ':', '"",')
            else:
                resultadossss = ""
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
                    filtro_oleo_strsss = ', '.join(FluidoCambioManual)

                    # Exibe a string resultante
                    print('"FluidoCambioManual"',':','"',filtro_oleo_strsss,'",')
                    print('"QuantidadeFluidoCambioManual"',':','"','",')
                    

                else:
                    filtro_oleo_strsss =""
                    print('"FiltroCambioAutomatico"', ':', '"",')
                    print('"QuantidadeFluidoCambioManual"',':','"','",')
            else:
                filtro_oleo_strsss =""
                print('"FluidoCambioManual"', ':', '"",')
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
                    filtro_oleo_strssss = ', '.join(OleoDiferencialTraseiro)

                    # Exibe a string resultante
                    print('"OleoDiferencialTraseiro"',':','"',filtro_oleo_strssss,'",')
                    print('"QuantidadeOleoDiferencialTraseiro"',':','"','",')

                else:
                    filtro_oleo_strssss =""
                    print('"OleoDiferencialTraseiro"', ':', '"",')
                    print('"QuantidadeOleoDiferencialTraseiro"',':','"','",')
            else:
                filtro_oleo_strssss=""
            print('"teste"', ':', '"",')
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
                    resultadosssss = ", ".join([f"{elementos[i]} {elementos[i+1]}" for i in range(0, len(elementos), 2)])
                    
                    # Exibe a string resultante
                    print('"AditivoRadiador"', ':', '"', resultadosssss, '",')
                    print('"QuantidadeAditivoRadiador"', ':', '"', '",')
                else:
                    resultadosssss =" "
                    print('"AditivoRadiador"', ':', '"",')
                    print('"QuantidadeAditivoRadiador"', ':', '"",')
            else: 
                resultadosssss =" "
                print('"AditivoRadiador"', ':', '"",')
                print('"QuantidadeAditivoRadiador"', ':', '"",')
        
            print('"teste1"', ':', '"",')
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
                    filtro_oleo_strsssss = ', '.join(FluidoFreio)

                    # Exibe a string resultante
                    print('"FluidoFreio"',':','"',filtro_oleo_strsssss,'",')
                    print('"QuantidadeFluidoFreio"',':','"1,0",')

                else:
                    print('"OleoDiferencialTraseiro"', ':', '"",')
                    print('"QuantidadeFluidoFreio"',':','"','",')            
            else:
                filtro_oleo_strsssss=" "
                print('"FluidoFreio"', ':', '"",')

        
        
            print('"teste2"', ':', '"",')
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
                    filtro_oleo_strssssss = ', '.join(FluidoDirecao)

                    # Exibe a string resultante
                    print('"FluidoDirecao"',':','"',filtro_oleo_strssssss,'",')
                    print('"QuantidadeFluidoDirecao"',':','"1,0"')
                else:
                    print('"FluidoDirecao"', ':', '" ",')
            else:
                filtro_oleo_strssssss=""
                print('"FluidoFreio"', ':', '" ",')


            print('"teste3"', ':', '"",')
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
                    filtro_oleo_strssssss = ', '.join(FluidoDirecao)

                    # Exibe a string resultante
                    print('"FluidoDirecao"',':','"',filtro_oleo_strssssss,'",')
                    print('"QuantidadeFluidoDirecao"',':','"1,0"')

                else:
                    filtro_oleo_strssssss = ""
                    print('"FluidoDirecao"', ':', '"",')

            dados_veiculo = {
                    "Marca": " ",
                    "Modelo": veiculo_nome_selenium_linha_unica,
                    "Ano": anos_sequenciais_str,
                    "OleoMotor": marcas_oleo_str,
                    "QuantidadeOleoMotor": litros_text_selenium,
                    "FiltroOleo": resultado_filtro_oleo_str,
                    "FiltroArMotor": resultado,
                    "PalhetaLimpadorDianteira": resultados,
                    "FiltroCombustivel": resultadoss,
                    "FiltroCabine": resultadosss,
                    "FluidoCambioAutomatico": filtro_oleo_strs,
                    "QuantidadeFluidoCambioAutomatico": " ",
                    "FiltroCambioAutomatico": resultadossss,
                    "FluidoCambioManual": filtro_oleo_strss,
                    "QuantidadeFluidoCambioManual": " ",
                    "OleoDiferencialTraseiro": filtro_oleo_strsss,
                    "QuantidadeOleoDiferencialTraseiro": " ",
                    "AditivoRadiador": resultadosssss,
                    "QuantidadeAditivoRadiador": " ",
                    "FluidoFreio": filtro_oleo_strsssss,
                    "QuantidadeFluidoFreio": "1,0",
                    "FluidoDirecao": filtro_oleo_strssssss,
                    "QuantidadeFluidoDirecao": "1,0",
                }
            print(dados_veiculo)
            json_data = json.dumps(dados_veiculo, ensure_ascii=False, indent=4)
            url = "https://reviselubapi.com.br/register/veiculo"
            headers = {
                "Content-Type": "application/json",

            }

            response = requests.post(url, headers=headers, data=json_data)
            if response.status_code == 200 or response.status_code == 201:
                print("✅ Dados enviados com sucesso!")
            else:
                print(f"❌ Erro ao enviar os dados: {response.status_code}")
                print(response.text)

    except Exception as e:
            print("Erro:", e)

    finally:
            # Fecha o navegador
            driver.quit()
            
            # Salva os dados no arquivo de texto
            with open("saida_dados.txt", "w", encoding="utf-8") as f:
                for line in output:
                    f.write(line + "\n")

    print("Dados salvos em 'saida_dados.txt'")