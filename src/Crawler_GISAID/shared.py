from __future__ import annotations

__all__ = [
    "IPipeline",
]
import abc
from typing import Dict, List, Union
import argparse

class IPipeline(abc.ABC):
    """
    Use it as a function
    """
    @classmethod
    def setup_parser(
        cls,
        parser: Union[argparse.ArgumentParser, None] = None,
    ) -> argparse.ArgumentParser:
        if parser is None:
            parser = argparse.ArgumentParser(
                prog=__file__,
                description=cls.__name__,
                formatter_class=argparse.RawTextHelpFormatter,
            )
        return parser

    @abc.abstractmethod
    def __new__(cls, *args, **kwargs):
        """
        function of pipeline
        """
        pass