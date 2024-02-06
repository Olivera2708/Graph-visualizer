import pkg_resources
from django.apps import AppConfig

from core.models import Workspace


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

    def remove_workspace(self, name):
        self.workspaces = [workspace for workspace in self.workspaces if workspace.name != name]

    def select_workspace(self, name: str):
        for ws in self.workspaces:
            if ws.name == name:
                self.selected_workspace = ws
                break

    def get_tabs(self):
        return [(ws.name, ws.id == self.selected_workspace.id) for ws in self.workspaces]


    def update_workspace(self, search_param: str = '', filter_params: list[str] = None, root_node: str = ''):
        if self.selected_workspace is not None:
            self.selected_workspace.update(search_param, filter_params, root_node)



def load_plugins_from_group(name: str):
    plugins = []
    print(f"Loading {name} plugins...")
    for entry in pkg_resources.iter_entry_points(group=name):
        print(f"Found {entry.name} plugin")
        p = entry.load()
        plugin = p()
        plugins.append(plugin)
    return plugins