from ..apibase import SlobsBase
from .selectionbase import SelectionBase
from .factories import register

# Design note: In practice, Selections do not have real source_ids or ids, and have a
# resourceId of 'Selection[]'.
# Rather than calling them an instance of SlobsClass, falling back to SlobsBase.

{
    "_type": "HELPER",
    "resourceId": "Selection[]",
    "lastSelectedId": "d85a672a-41a2-49c5-8e7f-201cd8dbfbec",
    "selectedIds": [
        "ccefc122-e8e6-4982-b2e6-6dd4e5da70ef",
        "55a35a1a-a5b3-42bd-9df7-b6cd6bae020f",
        "d85a672a-41a2-49c5-8e7f-201cd8dbfbec",
    ],
}


class Selection(SlobsBase, SelectionBase):
    def __init__(self, connection, resource_id):
        SlobsBase.__init__(self, connection, resource_id=resource_id)
        SelectionBase.__init__(self)


register(Selection)
