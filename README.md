# gmapsextractor
Extrai resultados de busca do Google Maps e retorna um GeoDataFrame
Utiliza as bibliotecas selenium, pandas, geopandas e shapely, bem como arcpy (para a ferramenta ArcGIS)
Verifique a documentação da biblioteca Selenium para download e utilização do driver correspondente ao seu navegador.

### Recebe:
busca = string com o termo a ser pesquisado no google maps. No exemplo abaixo foi utilizado "bares na asa norte brasília"
nome_layer_de_saida = string com o nome da layer de saída que será plotada no mapa do ArcGIS Pro (somente para ferramenta arcgis)

## Resultado:
![Captura de tela 2023-04-07 120010](https://user-images.githubusercontent.com/102811643/230632878-0470163d-3972-4e11-a9e5-9ade363ec4ec.png)

Mudando a simbologia para mapa de calor:
![Captura de tela 2023-04-07 115930](https://user-images.githubusercontent.com/102811643/230632924-b3832b84-3885-4d1a-a9c1-465523a8697e.png)
