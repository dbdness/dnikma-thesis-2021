from nubia import context


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

    # def set_db(self, db):
    #     self.obj = db
    #
    # def get_db(self):
    #     return self.obj
