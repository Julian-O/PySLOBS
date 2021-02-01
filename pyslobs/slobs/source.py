from __future__ import annotations  # Postponed eval of annotations. Fixed in 3.10
from typing import Optional, Any, Dict

from .typedefs import TObsFormData, TSourceType, ISourceModel
from ..apibase import SlobsClass
from .factories import source_factory, register

class Source(SlobsClass):
    # There is an undocumented Configurable field. Sharing here without knowing what
    # it means.

    def __init__(
        self,
        connection,
        resource_id: str,
        source_id: str,
        async_: bool,
        audio: bool,
        channel: Optional[int],
        configurable: Optional[bool],
        do_not_duplicate: bool,
        height: float,
        id_: str,
        muted: bool,
        name_: str,
        type_: TSourceType,
        video: bool,
        width: float,
    ):
        super().__init__(connection, resource_id=resource_id, source_id=source_id)

        self._async = async_
        self._audio = audio
        self._channel = channel
        self._configurable = configurable
        self._do_not_duplicate = do_not_duplicate
        self._height = height
        self._id = id_
        self._muted = muted
        self._name = name_
        self._type = type_
        self._video = video
        self._width = width
        # Warning may be out of date if changed on the server.

    def __str__(self):
        return f"{self.__class__.__name__}({self._source_id}, {self._name!r})"

    @property
    def async_(self):
        return self._async

    @property
    def audio(self):
        return self._audio

    @property
    def channel(self):
        return self._channel

    @property
    def configurable(self):
        return self._configurable

    @property
    def do_not_duplicate(self):
        return self._do_not_duplicate

    @property
    def height(self):
        return self._height

    @property
    def id(self):
        return self._id

    @property
    def muted(self):
        return self._muted

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    @property
    def video(self):
        return self._video

    @property
    def width(self):
        return self._width

    async def duplicate(self) -> Source:
        response = await self._connection.command("duplicate", self._prepared_params())
        return source_factory(self._connection, response)

    async def get_model(self) -> ISourceModel:
        response = await self._connection.command("getModel", self._prepared_params())
        return ISourceModel(
            async_=response["async"],
            audio=response["audio"],
            channel=response.get("channel", None),
            do_not_duplicate=response["doNotDuplicate"],
            height=response["height"],
            id=response["id"],
            muted=response["muted"],
            name=response["name"],
            source_id=response["sourceId"],
            type_=response["type"],
            video=response["video"],
            width=response["width"],
        )

    async def get_properties_form_data(self) -> TObsFormData:
        response = await self._connection.command(
            "getPropertiesFormData", self._prepared_params()
        )
        return response

    async def get_settings(self) -> Dict[Any]:
        response = await self._connection.command(
            "getSettings", self._prepared_params()
        )
        return response

    async def has_props(self) -> bool:
        response = await self._connection.command("hasProps", self._prepared_params())
        return response

    async def refresh(self) -> None:
        response = await self._connection.command("refresh", self._prepared_params())
        self._check_empty(response)

    async def set_name(self, new_name) -> None:
        response = await self._connection.command(
            "setName", self._prepared_params([new_name])
        )
        self._check_empty(response)

    async def set_properties_form_data(self, properties: TObsFormData) -> None:
        response = await self._connection.command(
            "setPropertiesFormData", self._prepared_params([properties])
        )
        self._check_empty(response)

    async def update_settings(self, settings: Dict[Any]) -> None:
        response = await self._connection.command(
            "updateSettings", self._prepared_params([settings])
        )
        self._check_empty(response)

register(Source)