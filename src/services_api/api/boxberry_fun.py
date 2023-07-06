import mysql.connector

from app.settings import BOXBERRY_FUN_HOST, BOXBERRY_FUN_LOGIN, BOXBERRY_FUN_PORT, \
    BOXBERRY_FUN_PASSWORD, BOXBERRY_FUN_DB_NAME


class BoxberryFun:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=BOXBERRY_FUN_HOST,
            user=BOXBERRY_FUN_LOGIN,
            port=BOXBERRY_FUN_PORT,
            passwd=BOXBERRY_FUN_PASSWORD,
            database=BOXBERRY_FUN_DB_NAME,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def get_cdek_city_codes(self):
        request = f"SELECT code, cdek_code FROM statistic_cities sc WHERE sc.cdek_code IS NOT NULL"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes

    def get_parser_groups(self):
        request = f"SELECT * FROM parser_parsinggroups"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes

    def get_parser_groups_city(self):
        request = f"SELECT * FROM parser_parsinggroups_city"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes

    def get_parser_groups_routes(self):
        request = f"SELECT * FROM parser_parsinggroups_routes"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes

    def get_city_code_by_id(self, city_id):
        request = f"SELECT code FROM statistic_cities WHERE id={city_id}"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes[0]

    def get_tariffs_groups(self):
        request = f"SELECT * FROM parser_deliveryservicestariffs_parsing_groups"
        self.cursor.execute(request)
        cdek_codes = self.cursor.fetchall()
        return cdek_codes

    def get_tariff(self, tariff_id):
        request = f"SELECT pd.code FROM parser_deliveryservicestariffs pd WHERE pd.id={tariff_id}"
        self.cursor.execute(request)
        tariff_code = self.cursor.fetchall()
        return tariff_code[0][0]