from typing import Optional, Dict, List

from ..apibase import SlobsService, Event
from .source import Source
from .typedefs import TSourceType, IObsListOption, ISourceAddOptions
from .factories import source_factory


class SourcesService(SlobsService):
    def __init__(self, connection):
        super().__init__(connection)

        self.source_added = Event(connection, "sourceAdded", self.__class__.__name__)

        self.source_removed = Event(
            connection, "sourceRemoved", self.__class__.__name__
        )

        self.source_updated = Event(
            connection, "sourceUpdated", self.__class__.__name__
        )

    async def add_file(self, path: str) -> Source:
        response = await self._connection.command(
            "addFile", self._prepared_params([str(path)])
        )
        return source_factory(self._connection, response)

    async def create_source(
        self,
        name: str,
        type_: TSourceType,
        settings: Optional[Dict],
        options: Optional[ISourceAddOptions],
    ) -> Source:
        options_dict = (
            {}
            if not options
            else {"channel": options.channel, "isTemporary": options.is_temporary}
        )
        response = await self._connection.command(
            "createSource",
            self._prepared_params([name, type_, settings, options_dict]),
        )
        return source_factory(self._connection, response)

    async def get_available_sources_types_list(self) -> list[any]:
        response = await self._connection.command(
            "getAvailableSourcesTypesList", self._prepared_params([])
        )
        return [
            IObsListOption(value=subitem["value"], description=subitem["description"])
            for subitem in response
        ]

    async def get_source(self, source_id: str) -> Source:
        response = await self._connection.command(
            "getSource", self._prepared_params([source_id])
        )
        return source_factory(self._connection, response)

    async def get_sources(self) -> List[Source]:
        response = await self._connection.command(
            "getSources", self._prepared_params([])
        )
        return [source_factory(self._connection, subitem) for subitem in response]

    async def get_sources_by_name(self, name: str) -> List[Source]:
        response = await self._connection.command(
            "getSourcesByName", self._prepared_params([name])
        )
        return [source_factory(self._connection, subitem) for subitem in response]

    async def remove_source(self, id_: str) -> None:
        response = await self._connection.command(
            "removeSource", self._prepared_params([id_])
        )
        self._check_empty(response)

    async def show_add_source(self, source_type: TSourceType) -> None:
        """
        Causes the UI to open the Add Source dialog box, at the point where
        the source-type has been selected and a name is to be entered.
        """
        response = await self._connection.command(
            "showAddSource", self._prepared_params([source_type])
        )
        self._check_empty(response)

    async def show_showcase(self) -> None:
        """
        Causes the UI to open the Add Source dialog box, at the point where
        the source-type is to be selected.
        """
        response = await self._connection.command(
            "showShowcase", self._prepared_params([])
        )
        self._check_empty(response)

    async def show_source_properties(self, source_id: str) -> Source:
        """
        Causes the UI to open the settings dialog box on the selected source.
        """
        response = await self._connection.command(
            "showSourceProperties", self._prepared_params([source_id])
        )
        self._check_empty(response)
