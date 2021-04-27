import logging

import mysql.connector

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MySQLConn(object):
    def __init__(self):
        self.conn = None
        self.curs = None

    def connect(self, conn_args: dict = None):
        if self.conn is None:
            if conn_args is None:
                raise Exception("No connection arguments provided, and MySQL connection is none.\n",
                                "Please provide connection kwargs.")
            try:
                self.conn = mysql.connector.connect(**conn_args)
                self.curs = self.conn.cursor()
                self.curs.execute('SELECT VERSION()')
                self.curs.fetchone()
                logger.info("MySQL connection to database established.")
                logger.info("Connection details:")
                logger.info(f'{conn_args}')
            except(Exception, mysql.connector.Error) as ex:
                logger.error("Error establishing MySQL connection:")
                logger.error(ex)
        return self

    def query(self, sql: str, params: tuple = None):
        """
        Send a query to the open MySQL connection.
        :param sql: The MySQL query to be executed.
        :param params: (Optional) Parameters/arguments for the query.
        :return: A cursor object containing query results, if any.
        You can fetch results with fetchone(), fetchall()
        or directly iterate the results with

        for(first_name, last_name) in curs:
            print(first_name, last_name)
        """
        if self.conn is None:
            raise Exception("MySQL connection is None, cannot execute query.",
                            "Please run the connect() function first.")
        self.curs.execute(sql, params)
        logger.debug(self.curs.statement)
        return self.curs


mysql_conn = MySQLConn()
