from ..apibase import SlobsService
from .selectionbase import SelectionBase


class SelectionService(SlobsService, SelectionBase):
    def __init__(self, connection):
        SlobsService.__init__(self, connection)
        SelectionBase.__init__(self)
