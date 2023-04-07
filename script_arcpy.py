"""
Script que mapeia estabelecimentos de uma determinada região com base no termo de busca do google maps
Recebe
    busca: string com termo de busca utilizado para a pesquisa no google maps
    nome_layer_de_saida: string com nome da layer que será inserida no mapa
"""
import arcpy
import time
import pandas as pd
import geopandas as gpd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from shapely import Point

def script_tool(busca, nome_arquivo_de_saida):
    """Script code goes below"""
    # Parâmetros
    busca = arcpy.GetParameterAsText(0) ############
    
    # Define as configurações do driver do Selenium para o Edge
    path_to_driver = '''C:Caminho\Para\O\Driver\Do\Seu\Navegador.exe'''
    service = Service(path_to_driver)
    driver = webdriver.Edge(service=service)     # Substituir pelo seu navegador de escolha (verifique documentação da biblioteca selenium)
    driver.get("https://www.google.com/maps")
    time.sleep(3)
    
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(busca)
    search_box.send_keys(Keys.ENTER)
    
    # Espera alguns segundos para a página carregar
    time.sleep(3)
    
    # Scroll 5x
    results_panel = driver.find_element(By.XPATH, '//div[@role="feed"]')
    contador_scroll = 0
    while contador_scroll <= 20:  
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
        time.sleep(2.5)
        contador_scroll += 1
    
    # Aguardando carregar os resultados
    time.sleep(2)
    
    # Resultados da busca
    search_results = driver.find_elements(By.XPATH, '//div[@role="article"]')
    
    # Instanciando GeoDataFrame
    gdf_resultados = gpd.GeoDataFrame(columns=['nome', 'n_estrelas', 'n_coment', 'preco', 'geometry'])
    
    # Captura de atributos
    idx_resultado = 0
    for result in search_results:
        try:
            link = result.find_element(By.CSS_SELECTOR, 'a')
            nome = link.get_attribute("aria-label")
            href = link.get_attribute("href")
            
            avaliacao = result.find_elements(By.CSS_SELECTOR, 'span[role="img"]')
            numero_elementos = 0
            for texto in avaliacao:
                numero_elementos += 1
                if numero_elementos == 1:
                    texto_sep = texto.get_attribute('aria-label').split(' ')
                    estrelas = float(texto_sep[0].replace(',', '.'))
                    comentarios = int(texto_sep[2].replace('.', ''))
                    preco, cifroes = None, None
                elif numero_elementos == 2:
                    texto_sep = texto.get_attribute('aria-label').split(' ')
                    preco = texto_sep[1]
                    if preco == 'Barato':
                        cifroes = 1
                    elif preco == 'Moderado':
                        cifroes = 2
                    elif preco == 'Caro':
                        cifroes = 3
                    else:
                        cifroes = 4
    
            lat = float(href.split('!')[5].split('d')[1])
            lon = float(href.split('!')[6].split('d')[1])
    
            arcpy.AddMessage(nome)
            arcpy.AddMessage(estrelas)
            arcpy.AddMessage(comentarios)
            arcpy.AddMessage(preco)
            arcpy.AddMessage(lat)
            arcpy.AddMessage(lon)
            arcpy.AddMessage('')
    
            gdf_resultados.loc[idx_resultado, 'nome'] = nome
            gdf_resultados.loc[idx_resultado, 'n_estrelas'] = estrelas
            gdf_resultados.loc[idx_resultado, 'n_coment'] = comentarios
            gdf_resultados.loc[idx_resultado, 'preco'] = cifroes
            gdf_resultados.loc[idx_resultado, 'geometry'] = Point(lon, lat)
    
            idx_resultado += 1
        except Exception as e:
            print(e)
    
    driver.quit()
    
    # Exibindo as camadas no mapa
    gdf_resultados = gdf_resultados.set_geometry('geometry').set_crs('epsg:4326')
    gdf_resultados.to_file('resultados.geojson')
    geojson_resultados = arcpy.conversion.JSONToFeatures('resultados.geojson', nome_layer_de_saida, geometry_type='POINT')
    
    # Adicionando ao mapa
    aprx = arcpy.mp.ArcGISProject('CURRENT')
    m = aprx.listMaps("Map")[0]
    
    return m.addDataFromPath(str(geojson_resultados))

if __name__ == "__main__":
    busca = arcpy.GetParameterAsText(0)
    nome_layer_de_saida = arcpy.GetParameterAsText(1)
    script_tool(busca, nome_layer_de_saida)
    
    # Mensagens
    arcpy.AddMessage('Processamento concluído com sucesso')
