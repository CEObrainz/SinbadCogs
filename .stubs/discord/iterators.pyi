import abc

from .user import User
from .member import Member
from .message import Message
from .audit_logs import AuditLogEntry
from .guild import Guild
from .http import _GuildDict, _GuildMemberDict
from .object import Object

from typing import Any, Optional, Union, TypeVar, List, Generic, Coroutine, Callable
from typing_extensions import Final

OLDEST_OBJECT: Final[Object] = ...

_IT = TypeVar('_IT')
_AIT = TypeVar('_AIT', bound=_AsyncIterator)
_VT = TypeVar('_VT')

class _AsyncIterator(Generic[_IT]):
    @abc.abstractmethod
    async def next(self) -> _IT: ...
    def get(self, **attrs: Any) -> Coroutine[Any, Any, Optional[_IT]]: ...
    async def find(self, predicate: Callable[[_IT], bool]) -> Optional[_IT]: ...
    def map(self, func: Callable[[_IT], Union[_IT, Coroutine[Any, Any, _IT]]]) -> _MappedAsyncIterator[_IT]: ...
    def filter(self,
               predicate: Callable[[_IT], Union[_IT, Coroutine[Any, Any, _IT]]]) -> _FilteredAsyncIterator[_IT]: ...
    async def flatten(self) -> List[_IT]: ...
    def __aiter__(self: _AIT) -> _AIT: ...
    async def __anext__(self) -> _IT: ...

def _identity(x: _VT) -> _VT: ...

class _MappedAsyncIterator(_AsyncIterator[_IT]):
    async def next(self) -> _IT: ...

class _FilteredAsyncIterator(_AsyncIterator[_IT]):
    async def next(self) -> _IT: ...

class ReactionIterator(_AsyncIterator[Union[User, Member]]):
    async def next(self) -> Union[User, Member]: ...
    async def fill_users(self) -> None: ...

class HistoryIterator(_AsyncIterator[Message]):
    async def next(self) -> Message: ...
    async def flatten(self) -> List[Message]: ...
    async def fill_messages(self) -> None: ...

class AuditLogIterator(_AsyncIterator[AuditLogEntry]):
    async def next(self) -> AuditLogEntry: ...

class GuildIterator(_AsyncIterator[Guild]):
    async def next(self) -> Guild: ...
    def create_guild(self, data: _GuildDict) -> Guild: ...
    async def flatten(self) -> List[Guild]: ...
    async def fill_guilds(self) -> None: ...

class MemberIterator(_AsyncIterator[Member]):
    async def next(self) -> Member: ...
    async def fill_members(self) -> None: ...
    async def create_member(self, data: _GuildMemberDict) -> Member: ...