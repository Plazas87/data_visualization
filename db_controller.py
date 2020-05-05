#! usr/bin/env python3

import psycopg2 as db
import logging
from built_configuration import BuildConfiguration


class DatabaseController:
    # Singleton implementation
    """Clase que controla la conexión a la base de datos. Esta implementación asegura que únicamente exista un objeto
    de esta clase, es decir, una sola conexión a la base de datos."""
    def __init__(self, configuration):
        logging.info('Starting database controller')
        self.user = configuration.user
        self.__password = configuration.password
        self.address = configuration.address
        self.port = configuration.port
        self.database = configuration.database

    def __new__(cls, name=None, params=None):
        if not hasattr(cls, 'instance'):  # Si no existe el atributo “instance”
            cls.instance = super(DatabaseController, cls).__new__(cls)  # lo creamos
        return cls.instance

    def connect(self, process_information='put some here'):
        try:
            # connect to the PostgreSQL server
            conn = None
            conn = db.connect(user=self.user,
                              password=self.__password,
                              host=self.address,
                              port=self.port,
                              database=self.database)
            return conn
        except Exception as e:
            logging.error('Unable to connect' + str(e))
            return None

    def close_connection(self, connection):
        """Termina la conexión con la base de datos. Esta función de ser llamada siempre despues de cualquier
        operación en la base de datos"""
        try:
            connection.close()
        except Exception as e:
            logging.error('Unable to close the connection: {}'.format(e))
            return None

    def selectQuery(self, table_name, *args, info=None, **kwargs):
        """Este método se encarga de realizar las consultas a todas las tablas de la base de datos del proyecto. Es lo
        suficientemente versatil como para entender varios tipos de consultas a las diferentes tablas"""
        query = []
        cursor = ''
        conn = ''
        str_query = ''
        data = ()
        data = (kwargs['year'], kwargs['month'], kwargs['station'], kwargs['magnitude'])
        str_query = """select m.station_id, s.latitude, s.longitude, m.time_id, d.day, d.month, d.year, m.value, m.magnitude_id from measurement m
                        join day d ON d.day_id = m.day_id
                        join station s ON m.station_id = s.station_id
                        where d.year = %s and d.month = %s and m.station_id = %s and m.magnitude_id = %s
                        order by d.year, d.month, d.day_id, m.time_id;"""

        if str_query != '':
            try:
                conn = self.connect(process_information=info)
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute(str_query, data)
                    qu = cursor.fetchall()
                    # qu = list(cursor.fetchall())
                    # for i in qu:
                    #     query.append([i])
            except Exception as e:
                print(e)
                cursor.close()
                self.close_connection(conn)
                logging.info('PostgreSQL connection has been closed but an Exception has been raised')
                return None
            else:
                cursor.close()
                self.close_connection(conn)
                logging.info('PostgreSQL connection is closed')
                return qu

        else:
            return None


if __name__ == '__main__':
    config = BuildConfiguration()
    dbController = DatabaseController(config)

    try:
        query = dbController.selectQuery('measurement', 'station_id', 'day_id', 'time_id', 'magnitude_id', 'value',
                                         month='1',
                                         year='2016',
                                         station='28079035',
                                         magnitude='8',
                                         info='Get measurement data')
    except Exception as e:
        print(type(e))
        print(e)

    print(query)
