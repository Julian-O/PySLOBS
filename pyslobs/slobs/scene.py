from typing import Optional, Any
from ..apibase import SlobsClass
from .scenenode import (
    SceneNode,
)
from .factories import (
    scenenode_factory,
    sceneitem_factory,
    sceneitemfolder_factory,
    selection_factory,
    source_factory,
    register,
)
from .typedefs import ISceneNodeAddOptions, ISourceAddOptions, TSourceType


class Scene(SlobsClass):
    def __init__(
        self,
        connection,
        resource_id: str,
        source_id: str,
        id: str,
        name: str,
        nodes: list[SceneNode],
    ):
        super().__init__(connection, resource_id=resource_id, source_id=source_id)

        self._name = name
        # Warning may be out of date if changed on the server.
        # Use set_name to change

        self._id = id
        self._nodes = nodes

    def __str__(self):
        return f"{self.__class__.__name__}({self._resource_id}, {self.name!r})"

    @property
    def name(self):
        return self._name

    @property
    def nodes(self):
        return self._nodes

    @property
    def id(self):
        return self._id

    async def add_file(self, path, folder_id: Optional[str] = None) -> SceneNode:
        response = await self._connection.command(
            "addFile", self._prepared_params([str(path), folder_id])
        )
        raise scenenode_factory(self._connection, response)

    async def add_source(
        self, source_id: str, options: Optional[ISceneNodeAddOptions]
    ) -> bool:
        options_dict = {}
        if options:
            if options.id is not None:
                option_dict["id"] = options.id
            if options.source_add_options is not None:
                source_add_options = {}
                if options.source_add_options.channel is not None:
                    source_add_options["channel"] = options.source_add_options.channel
                if options.source_add_options.is_temporary is not None:
                    source_add_options[
                        "isTemporary"
                    ] = options.source_add_options.is_temporary
                options_dict["sourceAddOptions"] = source_add_options
        response = await self._connection.command(
            "addSource", self._prepared_params([source_id, options_dict])
        )
        return response

    async def can_add_source(self, source_id: str) -> bool:
        response = await self._connection.command(
            "canAddSource", self._prepared_params([source_id])
        )
        return response

    async def clear(self):
        response = await self._connection.command("clear", self._prepared_params())
        self._check_empty(response)

    async def create_and_add_source(
        self, name: str, type_: TSourceType, settings: Optional[dict[Any]]
    ): # -> SceneItem:
        response = await self._connection.command(
            "createAndAddSource", self._prepared_params([name, type_, settings])
        )
        return sceneitem_factory(self._connection, response)

    async def create_folder(
        self, name: str, type_: TSourceType, settings: Optional[dict[Any]]
    ): # -> SceneItem:
        response = await self._connection.command(
            "createFolder", self._prepared_params([name, type_, settings])
        )
        return sceneitemfolder_factory(self._connection, response)

    async def get_folder(self, scene_folder_id: str):  # -> SceneItemFolder:
        response = await self._connection.command(
            "getFolder", self._prepared_params([scene_folder_id])
        )
        return sceneitemfolder_factory(self._connection, response)

    async def get_folders(self):  # -> list[SceneItemFolder]:
        response = await self._connection.command("getFolders", self._prepared_params())
        return [
            sceneitemfolder_factory(self._connection, subitem) for subitem in response
        ]

    async def get_item(self, scene_folder_id: str):  # -> SceneItem:
        response = await self._connection.command(
            "getItem", self._prepared_params([scene_folder_id])
        )
        return sceneitem_factory(self._connection, response)

    async def get_items(self):  # -> list[SceneItem]:
        response = await self._connection.command("getItems", self._prepared_params())
        return [sceneitem_factory(self._connection, subitem) for subitem in response]

    async def get_model(self):
        response = await self._connection.command("getModel", self._prepared_params())
        return scene_factory(self._connection, response)

    async def get_nested_items(self):  # -> Source
        response = await self._connection.command(
            "getNestedItems", self._prepared_params()
        )
        return [sceneitem_factory(self._connection, source) for source in response]

    async def get_nested_scenes(self):  # -> Source
        response = await self._connection.command(
            "getNestedScenes", self._prepared_params()
        )
        return [scene_factory(self._connection, source) for source in response]

    async def get_nested_sources(self):  # -> Source
        response = await self._connection.command(
            "getNestedSources", self._prepared_params()
        )
        return [source_factory(self._connection, source) for source in response]

    async def get_node(self, scene_node_id):  # -> Source
        response = await self._connection.command(
            "getNode", self._prepared_params([scene_node_id])
        )
        return scenenode_factory(self._connection, source)

    async def get_node_by_name(self, name: str):  # -> Source
        response = await self._connection.command(
            "getNodeByName", self._prepared_params([name])
        )
        return scenenode_factory(self._connection, source)

    async def get_nodes(self):  # -> Source
        response = await self._connection.command("getNodes", self._prepared_params())
        result = [scenenode_factory(self._connection, source) for source in response]
        # Update attributes as a side-effect
        self._nodes = result
        return result

    async def get_root_nodes(self):
        response = await self._connection.command(
            "getRootNodes", self._prepared_params()
        )
        return [scenenode_factory(self._connection, node) for node in response]

    async def get_selection(self, ids: Optional[list[str]]):
        response = await self._connection.command(
            "getSelection", self._prepared_params(ids)
        )
        return selection_factory(self._connection, response)

    async def get_source(self):
        response = await self._connection.command(
            "getSource", self._prepared_params()
        )
        return source_factory(self._connection, response)

    async def make_active(self):
        response = await self._connection.command("makeActive", self._prepared_params())
        self._check_empty(response)

    async def remove(self):
        response = await self._connection.command("remove", self._prepared_params())
        self._check_empty(response)

    async def remove_folder(self, folder_id):
        response = await self._connection.command("removeFolder", self._prepared_params([folder_id]))
        self._check_empty(response)

    async def remove_item(self, scene_item_id):
        response = await self._connection.command("removeItem", self._prepared_params([scene_item_id]))
        self._check_empty(response)

    async def set_name(self, new_name):
        response = await self._connection.command(
            "setName", self._prepared_params([new_name])
        )
        self._check_empty(response)

        # Update local cache.
        self._name = new_name


register(Scene)
