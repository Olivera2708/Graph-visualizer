import pkg_resources
from django.apps import AppConfig

from core.core.models import Workspace, Graph


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    data_source_plugins = []
    visualizer_plugins = []
    workspaces: list[Workspace] = []
    selected_workspace: Workspace = None


    def load_plugins(self):
        self.data_source_plugins = load_plugins_from_group("data_source")
        self.visualizer_plugins = load_plugins_from_group("visualizer")

    def add_workspace(self, data_source_id: str):
        workspace: Workspace = Workspace(data_source_id)
        self.workspaces.append(workspace)
        self.selected_workspace = workspace

    def remove_workspace(self, workspace):
        pass
        #id ili ceo

    def select_workspace(self, next: Workspace):
        self.selected_workspace = next
        #id ili ceo


    def update_workspace(self, data_source_id: str, search_param: str = '', filter_params: list = []):
        if self.workspaces:
            self.selected_workspace.update(data_source_id)
        else:
            self.add_workspace(data_source_id)



def load_plugins_from_group(name: str):
    plugins = []
    print(f"Loading {name} plugins...")
    for entry in pkg_resources.iter_entry_points(group=name):
        print(f"Found {entry.name} plugin")
        p = entry.load()
        plugin = p()
        plugins.append(plugin)
    return plugins