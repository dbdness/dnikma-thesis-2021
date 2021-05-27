import mysql.connector
from nubia import context

from dnikma_integrity_checker.helpers.utils import dicprint, Severity


class MySQLConn(object):

    def __init__(self):
        self._conn = None
        self._curs = None
        self._verbose = 0

    @property
    def verbose(self) -> int:
        try:
            self._verbose = context.get_context().args.verbose
        except:
            self._verbose = 0
        finally:
            return self._verbose

    def connect(self, conn_args: dict):
        """
        Connect to a specified MySQL instance.
        :param conn_args: Connection arguments in the format:
        {"host": "myHostAddress", "database": "myDatabase", "user": "myUsername", "password": "myPassword";
        :param verbose: Verbosity level. Accepts 1 or 0.
        :return: Connection wrapped in a MySQLConn object.
        """
        if self._conn is None:
            if conn_args is None:
                raise Exception("No connection arguments provided, and MySQL connection is none.\n",
                                "Please provide connection kwargs.")
            try:
                self._conn = mysql.connector.connect(**conn_args)
                self._conn.autocommit = True
                self._curs = self._conn.cursor()
                self._curs.execute('SELECT VERSION()')
                self._curs.fetchone()
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
        if self._conn is None:
            raise Exception("MySQL connection is None, cannot execute query. Please run the connect() function first.")

        if self.verbose:
            print()
            dicprint("SQL statement passed to driver:", Severity.INFO)
            dicprint(sql, Severity.INFO)
        self._curs.execute(sql, params, multi=multi)
        if self.verbose:
            print()
            dicprint('Statement executed:', Severity.INFO)
            dicprint(self._curs.statement, Severity.INFO)
        return self._curs


# Singleton initialization
mysql_conn = MySQLConn()
