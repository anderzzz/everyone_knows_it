"""CV data classes

"""
import json
from abc import ABC
from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Optional, List, Type, get_type_hints


@dataclass
class CVData(ABC):
    pass


def serialize_cv_data(cv_data: CVData) -> str:
    """Serialize a CV data object to a dictionary

    Args:
        cv_data (CVData): The CV data object to serialize.

    Returns:
        dict: The serialized CV data object.

    """
    return json.dumps(asdict(cv_data))


def dataclass_to_str(cv_data_cls: Type[CVData]) -> str:
    """Convert a dataclass to a string

    Args:
        cv_data_cls (CVData): The dataclass type to give a string representation.

    Returns:
        str: The string representation of the dataclass type.

    """
    if not is_dataclass(cv_data_cls):
        raise TypeError("Provided class is not a dataclass")

    annotations = get_type_hints(cv_data_cls)
    field_data = fields(cv_data_cls)

    lines = [f"class {cv_data_cls.__name__}:"]
    if cv_data_cls.__doc__:
        lines.append(f'    """{cv_data_cls.__doc__}"""')
        lines.append("")

    for field in field_data:
        type_hint = annotations[field.name]
        if field.default is not field.default_factory:
            default_val = field.default if field.default is not None else "None"
            line = f"    {field.name}: {type_hint} = {default_val}"
        elif field.default_factory is not None:
            line = f"    {field.name}: {type_hint} = {field.default_factory.__name__}()"
        else:
            line = f"    {field.name}: {type_hint}"
        lines.append(line)

    return "\n".join(lines)


@dataclass
class Biography(CVData):
    """Biography data class

    """
    name: str
    email: str
    about_me: str
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    blog_url: Optional[str] = None
    home_address: Optional[str] = None

    @staticmethod
    def build(**kwargs) -> 'Biography':
        return Biography(**kwargs)


@dataclass
class EducationUniversity:
    """Formal education data class (e.g. university, college)

    """
    university: str
    degree: str
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    start_month: Optional[str] = None
    end_month: Optional[str] = None
    grade: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    field: Optional[str] = None
    description: Optional[str] = None


@dataclass
class EducationOnline:
    """Online education data class (e.g. Coursera, Udemy)

    """
    platform: str
    educator: str
    course: str
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    start_month: Optional[str] = None
    end_month: Optional[str] = None
    grade: Optional[str] = None
    url_certificate: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Educations(CVData):
    """Collection of education data classes

    """
    formal_education_entries: List[EducationUniversity]
    mooc_education_entries: Optional[List[EducationOnline]] = None

    @staticmethod
    def build(**kwargs) -> 'Educations':
        return Educations(
            formal_education_entries=[EducationUniversity(**entry) for entry in kwargs['formal_education_entries']],
            mooc_education_entries=[EducationOnline(**entry) for entry in kwargs['mooc_education_entries']] if 'mooc_education_entries' in kwargs else None
        )


@dataclass
class Employment:
    """Employment data class

    """
    company: str
    title: str
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    start_month: Optional[str] = None
    end_month: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Employments(CVData):
    """Collection of employment data classes

    """
    employment_entries: List[Employment]

    @staticmethod
    def build(**kwargs) -> 'Employments':
        return Employments(
            employment_entries=[Employment(**entry) for entry in kwargs['employment_entries']]
        )


@dataclass
class Skill:
    """Skill data class

    """
    name: str
    level: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Skills(CVData):
    """Collection of skill data classes

    """
    skill_entries: List[Skill]

    @staticmethod
    def build(**kwargs) -> 'Skills':
        return Skills(
            skill_entries=[Skill(**entry) for entry in kwargs['skill_entries']]
        )


@dataclass
class Publication:
    """Publication data class

    """
    title: str
    authors: str
    date: str
    publication_name: str
    description: Optional[str] = None


@dataclass
class Publications(CVData):
    """Collection of publication data classes

    """
    publication_entries: List[Publication]

    @staticmethod
    def build(**kwargs) -> 'Publications':
        return Publications(
            publication_entries=[Publication(**entry) for entry in kwargs['publication_entries']]
        )
