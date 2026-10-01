from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SocialPlatformAdapter(ABC):
    platform_name: str = "base"

    @abstractmethod
    def connect(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def validate_content(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def publish(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_account_info(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_analytics(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError
