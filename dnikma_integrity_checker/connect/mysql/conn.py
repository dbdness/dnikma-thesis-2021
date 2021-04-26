import logging

import mysql.connector

from dnikma_integrity_checker.helpers.singleton_base import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@Singleton
class MySQLConn(object):

    def __init__(self, conn_args):
        # Singleton handling
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

    def __str__(self):
        return self.conn

    def query(self, query, params: tuple = None):
        """
        Send a query to the open MySQL connection.
        :param query: The MySQL query to be executed.
        :param params: (Optional) Parameters/arguments for the query.
        :return: A cursor object containing query results, if any.
        You can fetch results with fetchone(), fetchall()
        or directly iterate the results with

        for(first_name, last_name) in curs:
            print(first_name, last_name)
        """
        if not self.conn:
            raise Exception('MySQL connection is None, cannot execute query.')
        self.curs.execute(query, params)
        logger.debug(self.curs.statement)
        return self.curs

    # def __del__(self):
    #     self.curs.close()
    #     self.conn.close()
