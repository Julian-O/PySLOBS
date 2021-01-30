from ..apibase import SlobsService, Event


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
