from ..apibase import SlobsService, Event
from .scene import Scene
from .factories import scenenode_factory, scene_factory
from .typedefs import ISceneModel


class ScenesService(SlobsService):
    def __init__(self, connection):
        super().__init__(connection)

        self.item_added = Event(connection, "itemAdded", self.__class__.__name__)
        self.item_removed = Event(connection, "itemRemoved", self.__class__.__name__)
        self.item_updated = Event(connection, "itemUpdated", self.__class__.__name__)
        self.scene_added = Event(connection, "sceneAdded", self.__class__.__name__)
        self.scene_removed = Event(connection, "sceneRemoved", self.__class__.__name__)
        self.scene_switched = Event(
            connection, "sceneSwitched", self.__class__.__name__
        )

    async def active_scene(self):
        response = await self._connection.command(
            "activeScene", self._prepared_params()
        )
        return scene_factory(self._connection, response)

    async def active_scene_id(self):
        response = await self._connection.command(
            "activeSceneId", self._prepared_params()
        )
        return response

    async def create_scene(self, scene_name: str) -> Scene:
        response = await self._connection.command(
            "createScene", self._prepared_params([scene_name])
        )
        return scene_factory(self._connection, response)

    async def get_scene(self, scene_id: str) -> Scene:
        response = await self._connection.command(
            "activeScene", self._prepared_params([scene_id])
        )
        return scene_factory(self._connection, response)

    async def get_scenes(self):
        response = await self._connection.command("getScenes", self._prepared_params())
        return [scene_factory(self._connection, subitem) for subitem in response]

    # Warning: In Studio Mode, this won't take immediate effect.
    # See TransitionsService to detect Studio Mode and to execute the transition.
    async def make_scene_active(self, scene_id: str) -> bool:
        response = await self._connection.command(
            "makeSceneActive", self._prepared_params([scene_id])
        )
        return response

    async def remove_scene(self, id_: str) -> ISceneModel:
        response = await self._connection.command(
            "removeScene", self._prepared_params([id_])
        )
        return scene_factory(self._connection, response)
