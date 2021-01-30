"""
    The SLOBS API has concepts of
        * "Service"
            - top level entities can be instantiated at any time. They
              support methods and subscriptions.
        * "Class"
            - entities that are only instantiated by being returned from the
              server. They support methods and have some data attached.
        * "Interfaces"
            - entities that contain data but support no methods.
        * "Types"
            - restrictions on parameter values, like enumerated types.

    The Python API represents these internally as:
        * Service -> SlobsService
            - defined in this file.
        * Class -> SlobsClass
            - defined in this file.
        * Interface -> namedtuple
            - defined with the associated SlobsClasses
        * Types -> Enum types (and bool, str, int, float)
            - defined with the associated SlobsClasses
"""

from .connection import ProtocolError
from .pubsubhub import SubscriptionPreferences

"""
    Design note: Considered the use of CompactMode, which limits the number
    of fields returned when a new SlobsClass is introduced. 

    Pro: 
        * less processing per message
        * it avoids the issue of how to cache this data which may become
          obsolete without notice.

    Cons:
        * more round trips to gather basic information.
        * there doesn't appear to be a way to populate name fields otherwise.

    Compromise:
        * get all the fields, but only use the ones that appear as properties
          on the SlobsClasses.
"""


class SlobsBase:
    def __init__(self, connection, resource_id):
        self._connection = connection
        self._resource_id = resource_id

    def __str__(self):
        return f"{self.__class__.__name__}({self._resource_id})"

    # Helper functions.

    def _prepared_params(self, args=None):
        if args is None:
            args = []
        else:
            assert isinstance(args, list)
        return dict(resource=self._resource_id, args=args)

    @staticmethod
    def _check_empty(response):
        if response:
            raise ProtocolError("Expected void response: %s", response)


class SlobsService(SlobsBase):
    def __init__(self, connection):
        # This takes advantage of the fact that the Python class names
        # match the Javascript Resource names.
        super().__init__(connection, resource_id=self.__class__.__name__)


class SlobsClass(SlobsBase):
    """Base class for proxies to "Classes" in the data model

    Attributes are read-only, and are at risk of being out-of-date
    if there are changes to the server or to other instances referring
    to the same API entity.
    """

    """ 
        Design note: Ids.

        It doesn't appear to be well documented, but each SlobsClass has a
            source_id - a unique string, and a
            resource_id - which appears to be of the pp class_name["source_id"].

        Some SLobsClass also have an (unrelated?) field called "id".

        Each service just has a resource_id which is just the class name.

        It seems when referring to yourself, you have to provide the resource_id.
        When referencing associated SlobsClasses, you have to provide an "id" which 
        appears to actually be referring to the source_id.

    """

    def __init__(self, connection, resource_id, source_id):
        super().__init__(connection, resource_id)
        self._source_id = source_id

    @property
    def source_id(self):
        return self._source_id

    @property
    def resource_id(self):
        return self._resource_id

    def __str__(self):
        # Override to use source_id instead.
        return f"{self.__class__.__name__}({self._source_id})"


class _EventSubscription:
    def __init__(self, connection, resource_id, callback_coroutine):
        self._connection = connection
        self._resource_id = resource_id
        self._callback_coroutine = callback_coroutine

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.unsubscribe()

    async def unsubscribe(self):
        await self._connection.unsubscribe(self._resource_id, self._callback_coroutine)


class Event:
    """An event that can be subscribed to"""

    def __init__(self, connection, method: str, service: str):
        self._connection = connection
        self._service = service
        self._method = method

    async def subscribe(
        self, callback_coroutine, subscription_prefs=SubscriptionPreferences()
    ) -> _EventSubscription:
        subscription_resource_id = await self._connection.subscribe(
            method=self._method,
            params=dict(resource=self._service, args=[]),
            callback_coroutine=callback_coroutine,
            subscription_preferences=subscription_prefs,
        )

        return _EventSubscription(
            self._connection,
            subscription_resource_id,
            callback_coroutine,
        )
