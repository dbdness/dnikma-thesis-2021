from nubia import PluginInterface

from .dic_context import DicContext


class DicPlugin(PluginInterface):
    """
    The PluginInterface class is a way to customize nubia for every customer
    use case. It allows custom argument validation, control over command
    loading, custom context objects, and much more.

    In this case, the most important part is the application of our own, custom context.
    """

    def create_context(self):
        """
        Must create an object that inherits from `Context` parent class.
        The plugin can return a custom context but it has to inherit from the
        correct parent class.
        """
        return DicContext()
