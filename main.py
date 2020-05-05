import logging
import sys
import pandas as pd
from built_configuration import BuildConfiguration
from db_controller import DatabaseController
import folium


# Configuración del log de la aplicación
formatter = logging.basicConfig(level='DEBUG',
                                filename='log.txt',
                                filemode='a',
                                format='%(asctime)s;%(levelname)s;%(name)s;%(module)s;%(funcName)s;%(message)s')

rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
rootLogger.addHandler(consoleHandler)

if __name__ == '__main__':
    config = BuildConfiguration()
    dbController = DatabaseController(config)
    coordinates_madrid = [40.4167598, -3.7040395]

    try:
        query = dbController.selectQuery("measurement", info='Get measurement data',
                                         year=2016,
                                         month=1,
                                         station=28079035,
                                         magnitude=8)

    except Exception as e:
        print(type(e))
        print(e)

    cols = ['station_id', 'latitude', 'longitude', 'time', 'day', 'month', 'year', 'value', 'magnitude']
    query_data = pd.DataFrame(query, columns=cols)
    print(query_data.head())

    map_air = folium.Map(coordinates_madrid, zoom_start=13)
    map_air.save('mapa.html')

