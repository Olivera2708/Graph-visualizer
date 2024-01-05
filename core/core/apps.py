import pkg_resources
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    data_source_plugins = []
    visualizer_plugins = []

    def load_plugins(self):
        self.data_source_plugins = load_plugins_from_group("core.data_source")
        self.visualizer_plugins = load_plugins_from_group("visualizer")


def load_plugins_from_group(name: str):
    plugins = []
    for entry in pkg_resources.iter_entry_points(group=name):
        p = entry.load()
        # print("{} {}".format(entry.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins