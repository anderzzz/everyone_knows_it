"""Pipeline functionality

"""
from abc import ABC, abstractmethod
from typing import Any, List


class PipelineStep(ABC):
    @abstractmethod
    def process(self, inp: Any) -> Any:
        pass


class Pipeline:
    """Rudimentary pipeline class

    """
    def __init__(self, steps: List[PipelineStep]):
        self.steps = steps

    def run(self, inp: Any) -> Any:
        result = inp
        for step in self.steps:
            result = step.process(result)
        return result
