from sixectomy.models import Import
from sixectomy.models import TypeOfImport

without_six = [
    Import(module=[], name="requests",
           alias=None, typeof=TypeOfImport.DIRECT),
    Import(module=[], name="abc",
           alias=None, typeof=TypeOfImport.DIRECT),
    Import(module="foo", name="bar",
           alias=None, typeof=TypeOfImport.FROM),
]

with_six = [
    Import(
        module=[], name='requests', alias=None, 
        typeof=TypeOfImport.DIRECT
    ),
    Import(
        module=[], name='abc', alias=None, typeof=TypeOfImport.DIRECT
    ),
    Import(
        module=[], name='six', alias=None, typeof=TypeOfImport.DIRECT
    ),
    Import(
        module='six', name='parse', alias='urlparse',
        typeof=TypeOfImport.FROM
    ),
    Import(
        module='foo', name='bar', alias=None, typeof=TypeOfImport.FROM
    )
]
