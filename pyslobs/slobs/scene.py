from typing import Optional, Any
from ..apibase import SlobsClass
from .scenenode import (
    SceneNode,
)
from .factories import (
    scenenode_factory,
    sceneitem_factory,
    sceneitemfolder_factory,
    source_factory,
    register,
)
from .typedefs import ISceneNodeAddOptions, ISourceAddOptions


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

    async def add_file(
        self, path, folder_id: Optional[str] = None
    ) -> NotImplementedError:
        response = await self._connection.command(
            "addFile", self._prepared_params([str(path), folder_id])
        )
        raise NotImplementedError()

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

    # async def createAndAddSource
    # async def createFolder
    # async def getFolder
    # async def getFolders
    # async def getItem
    # async def getItems

    async def get_model(self):
        response = await self._connection.command("getModel", self._prepared_params())
        return scene_factory(self._connection, response)

    # async def getNestedItems
    # async def getNestedScenes

    # async def getNestedSources
    async def get_nested_sources(self):  # -> Source
        response = await self._connection.command(
            "getNestedSources", self._prepared_params()
        )
        return [source_factory(self._connection, source) for source in response]

    # async def getNode
    # async def getNodeByName
    # async def getNodes(refresh=True)
    async def get_root_nodes(self):
        response = await self._connection.command(
            "getRootNodes", self._prepared_params()
        )
        return [scenenode_factory(self._connection, node) for node in response]

    # async def getSelection
    # async def getSource

    async def make_active(self):
        response = await self._connection.command("makeActive", self._prepared_params())
        self._check_empty(response)

    # async def remove
    # async def removeFolder
    # async def removeItem

    async def set_name(self, new_name):
        response = await self._connection.command(
            "setName", self._prepared_params([new_name])
        )
        self._check_empty(response)

        # Update local cache.
        self._name = new_name


register(Scene)
