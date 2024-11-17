from abc import abstractmethod, ABC
from typing import Generic, TypeVar

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")


class AbstractRepository(Generic[M, K], ABC):
    """
    Absract representation of a repository
    """

    # Create a new instance of the Model
    @abstractmethod
    def create(self, instance: M) -> M:
        pass

    # Fetch an existing instance of the Model by it's unique Id
    @abstractmethod
    def get(self, id: K) -> M:
        pass

    # Delete an existing instance of the Model
    @abstractmethod
    def delete(self, id: K) -> None:
        pass

    # Lists all existing instance of the Model
    @abstractmethod
    def list(self, limit: int, start: int) -> list[M]:
        pass

    # Updates an existing instance of the Model
    @abstractmethod
    def update(self, id: K, instance: M) -> M:
        pass
