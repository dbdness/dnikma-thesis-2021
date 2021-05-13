from nubia import context

from dnikma_integrity_checker.commands.connect.mysql.mysql_conn import MySQLConn


class DicContext(context.Context):
    """
    This class overrides the standard Nubia context, allowing us to extend it to our needs.
    In this case, the most important extension is the introduction of a custom, context-passable object (obj).
    """

    # def on_connected(self, *args, **kwargs):
    #     pass

    def __init__(self):
        super().__init__()
        self.obj = {}

    def store_obj(self, key: str, obj):
        self.obj[key] = obj

    def get_obj(self, key):
        return self.obj.get(key)

    def get_mysql(self) -> MySQLConn:
        return self.obj.get('mysql')
