"""Data access object for the application.

Presently these are simple wrappers around the local data repositories.

The DAOs are where the knowledge of the raw data schema is encapsulated. Each type of
data to retrieve has its own DAO such that there is a single responsibility for each
DAO.

"""
from typing import Optional
from abc import ABC, abstractmethod

from ._local_data_repo import (
    registry_persons,
    registry_job_ads,
    registry_form_templates,
    registry_form_templates_toc,
)


class DAO(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get(self, *args, **kwargs) -> str:
        pass


class PersonsDAO(DAO):
    def __init__(self):
        super().__init__()
        self.registry = registry_persons

    def get_person(self, person: str) -> dict:
        return self.registry.get(person)

    def get(self, person: str, feature: str) -> str:
        return self.registry.get(person, feature)


class PersonsEducationDAO(PersonsDAO):
    def __init__(self):
        super().__init__()

    def get(self, person: str, feature: Optional[str] = None) -> str:
        return super().get(person, 'education')


class PersonsEmploymentDAO(PersonsDAO):
    def __init__(self):
        super().__init__()

    def get(self, person: str, feature: Optional[str] = None) -> str:
        return super().get(person, 'employment')


class PersonsSkillsDAO(PersonsDAO):
    def __init__(self):
        super().__init__()

    def get(self, person: str, feature: Optional[str] = None) -> str:
        return super().get(person, 'skills')


class PersonsPublicationsDAO(PersonsDAO):
    def __init__(self):
        super().__init__()

    def get(self, person: str, feature: Optional[str] = None) -> str:
        return super().get(person, 'publications')


class JobAdsDAO(DAO):
    def __init__(self):
        super().__init__()
        self.registry = registry_job_ads

    def get(self, company: str, position: str) -> str:
        return self.registry.get(company, position)


class FormTemplatesDAO(DAO):
    def __init__(self):
        super().__init__()
        self.registry = registry_form_templates

    def get(self, template_name: str) -> str:
        return self.registry.get(template_name)


class FormTemplatesTocDAO(DAO):
    def __init__(self):
        super().__init__()
        self.registry = registry_form_templates_toc

    def get(self, template_name: str, *args):
        return self.registry.get(template_name, *args)
