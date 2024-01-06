import pkg_resources
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    data_source_plugins = []
    visualizer_plugins = []

    def load_plugins(self):
        self.data_source_plugins = load_plugins_from_group("data_source")
        self.visualizer_plugins = load_plugins_from_group("visualizer")


def load_plugins_from_group(name: str):
    plugins = []
    print(f"Loading {name} plugins...")
    for entry in pkg_resources.iter_entry_points(group=name):
        print(f"Found {entry.name} plugin")
        p = entry.load()
        plugin = p()
        plugins.append(plugin)
    return plugins