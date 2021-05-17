import mysql.connector

from dnikma_integrity_checker.helpers.utils import dicprint, Severity


class MySQLConn(object):

    def __init__(self):
        self.conn = None
        self.curs = None
        self.verbose = 0

    def connect(self, conn_args: dict, verbose: int):
        """
        Connect to a specified MySQL instance.
        :param conn_args: Connection arguments in the format:
        {"host": "myHostAddress", "database": "myDatabase", "user": "myUsername", "password": "myPassword";
        :param verbose: Verbosity level. Accepts 1 or 0.
        :return: Connection wrapped in a MySQLConn object.
        """
        self.verbose = verbose
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
                if self.verbose:
                    print()  # Blank line for output prettify
                    dicprint("Connection details:", Severity.INFO)
                    dicprint(f'{conn_args}', Severity.INFO)
            except(Exception, mysql.connector.Error) as ex:
                dicprint(ex, Severity.ERROR)
        return self

    def query(self, sql: str, params=(), multi=False):
        """
        Send a query to the open MySQL connection.
        :param multi: Indicate if multiple statements are part of supplied SQL query.
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
            return None
        self.curs.execute(sql, params, multi=multi)
        if self.verbose:
            print()
            dicprint('Statement executed:', Severity.INFO)
            dicprint(self.curs.statement, Severity.INFO)
        return self.curs


# Singleton initialization
mysql_conn = MySQLConn()
