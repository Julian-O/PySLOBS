from ..apibase import SlobsClass
from .selectionbase import SelectionBase
from .factories import register


class Selection(SlobsClass, SelectionBase):
    def __init__(self, connection, resource_id, source_id):
        super(SlobsClass).__init__(
            connection, resource_id=resource_id, source_id=source_id
        )
        super(SelectionBase).__init__()


register(Selection)