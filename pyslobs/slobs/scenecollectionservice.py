from typing import Optional
from ..apibase import SlobsService, Event
from .typedefs import (
    ISceneCollectionsManifestEntry,
    ISceneCollectionSchema,
    ISceneCollectionCreateOptions,
)
from .factories import source_factory, sceneitem_factory


def iscenecollectionmanifestentry_factory(json_dict):
    return ISceneCollectionsManifestEntry(id=json_dict["id"], name=json_dict["name"])


def iscenecollectionschema_factory(connection, json_dict):
    return ISceneCollectionSchema(
        id=json_dict["id"],
        name=json_dict["name"],
        # The field is called scenes, but doesn't actually contain scenes.
        # Appears to be a novel type that references scenes. Returning the raw dict.
        scenes=json_dict["scenes"],
        # The field is called sources, but doesn't actually contain sources.
        # Appears to be a novel type that references sources. Returning the raw dict.
        sources=[json_dict["sources"]],
    )


class SceneCollectionsService(SlobsService):
    def __init__(self, connection):
        super().__init__(connection)

        self.collection_added = Event(
            connection, "collectionAdded", self.__class__.__name__
        )
        self.collection_removed = Event(
            connection, "collectionRemoved", self.__class__.__name__
        )
        self.collection_switched = Event(
            connection, "collectionSwitched", self.__class__.__name__
        )
        self.collection_updated = Event(
            connection, "collectionUpdated", self.__class__.__name__
        )
        self.collection_will_switch = Event(
            connection, "collectionWillSwitch", self.__class__.__name__
        )

    async def active_collection(self):
        response = await self._connection.command(
            "activeCollection", self._prepared_params([])
        )
        return iscenecollectionmanifestentry_factory(response)

    async def collections(self):
        response = await self._connection.command(
            "collections", self._prepared_params([])
        )
        return [iscenecollectionmanifestentry_factory(subitem) for subitem in response]

    async def create(self, options: ISceneCollectionCreateOptions):
        response = await self._connection.command(
            "create", self._prepared_params([{"name": options.name}])
        )
        return iscenecollectionmanifestentry_factory(response)

    async def delete(self, id: Optional[str]) -> None:
        response = await self._connection.command("delete", self._prepared_params([id]))
        self._check_empty(response)

    async def fetch_scene_collections_schema(self):
        # Note: Intermittently raises ProtocolError (code=-32600 INVALID_REQUEST)
        # possibly if called too quickly after other operations?
        response = await self._connection.command(
            "fetchSceneCollectionsSchema", self._prepared_params([])
        )
        return [
            iscenecollectionschema_factory(self._connection, subitem)
            for subitem in response
        ]

    async def load(self, id: str) -> None:
        response = await self._connection.command("load", self._prepared_params([id]))
        self._check_empty(response)

    async def rename(self, new_name: str, id: str) -> None:
        response = await self._connection.command(
            "rename", self._prepared_params([new_name, id])
        )
        self._check_empty(response)
