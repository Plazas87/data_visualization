#! usr/bin/env python3

from configparser import ConfigParser
import logging
import enums as conf


class BuildConfiguration:
    """Esta clase se encarga de leer el archivo de configuración genral, las parametros leidos son almacenados como
    propiedades del objeto que sera luego instanciado en la clase controller"""
    def __init__(self):
        logging.info("Built main configuration object")
        param = self.__config()
        self.user = param['postgresql'][conf.DBConfigEnum.user.name]
        self.password = param['postgresql'][conf.DBConfigEnum.password.name]
        self.address = param['postgresql'][conf.DBConfigEnum.address.name]
        self.port = param['postgresql'][conf.DBConfigEnum.port.name]
        self.database = param['postgresql'][conf.DBConfigEnum.database.name]

    def __config(self, section='postgresql', filename='conf/configpostgres.ini'):
        """Configura los parámetros para la conexión con la base de datos a través de la lectura de un
        archivo de configuración de extención .ini"""
        conf = ConfigParser()
        try:
            conf.read(filename)
            config_file_dict = {}
            tmp = {}
            for sect in conf.sections():
                params = conf.items(sect)
                for param in params:
                    tmp[param[0]] = param[1]

                config_file_dict[sect] = tmp
                tmp = {}

            return config_file_dict

        except Exception as e:
            print(e)

    def __str__(self):
        return 'user:' + ' ' + self.user + '\npassword:' + ' ' + self.password + '\naddress:' + ' ' + self.address + \
               '\nport:' + ' ' + self.port + '\ndatabase:' + ' ' + self.database


if __name__ == '__main__':
    c = BuildConfiguration()
    print(c)


