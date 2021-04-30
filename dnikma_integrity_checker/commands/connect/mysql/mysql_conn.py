import mysql.connector

from dnikma_integrity_checker.helpers.utils import dicprint, Severity


class MySQLConn(object):
    def __init__(self):
        self.conn = None
        self.curs = None

    def connect(self, conn_args, verbose: int):
        if self.conn is None:
            if conn_args is None:
                raise Exception("No connection arguments provided, and MySQL connection is none.\n",
                                "Please provide connection kwargs.")
            try:
                self.conn = mysql.connector.connect(**conn_args)
                self.conn.autocommit = True
                self.curs = self.conn.cursor()
                self.curs.execute('SELECT VERSION()')
                self.curs.fetchone()
                if verbose:
                    dicprint("Connection details:", Severity.INFO)
                    dicprint(f'{conn_args}', Severity.INFO)
            except(Exception, mysql.connector.Error) as ex:
                dicprint(ex, Severity.ERROR)
        return self

    def query(self, sql: str, verbose: int, params: tuple = None):
        """
        Send a query to the open MySQL connection.
        :param verbose: Verbosity level
        :param sql: The MySQL query to be executed.
        :param params: (Optional) Parameters/arguments for the query.
        :return: A cursor object containing query results, if any.
        You can fetch results with fetchone(), fetchall()
        or directly iterate the results with

        for(first_name, last_name) in curs:
            print(first_name, last_name)
        """
        if self.conn is None:
            dicprint("MySQL connection is None, cannot execute query. Please run the connect() function first.",
                     Severity.ERROR)
            return
        self.curs.execute(sql, params)
        if verbose:
            dicprint('Statement executed:', Severity.INFO)
            dicprint(self.curs.statement, Severity.INFO)
        return self.curs


mysql_conn = MySQLConn()
