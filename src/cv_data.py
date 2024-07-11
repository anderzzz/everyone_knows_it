"""CV data classes

"""
from abc import ABC
from dataclasses import dataclass
from typing import Optional, List, Dict, Union, Callable, Any


class CVData(ABC):
    """Abstract base class for CV data classes

    """
    pass


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


def create_biography(biography: Dict[str, str]):
    """Create a biography data class

    """
    return Biography(**biography)


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
    education_entries: List[Union[EducationUniversity, EducationOnline]]


def create_educations(
        formal_education_entries: List[Dict],
        mooc_education_entries: Optional[List[Dict]] = None,
):
    """Create a collection of education data classes

    """
    educations = []
    for entry in formal_education_entries:
        educations.append(EducationUniversity(**entry))
    if mooc_education_entries:
        for entry in mooc_education_entries:
            educations.append(EducationOnline(**entry))
    return Educations(education_entries=educations)


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


def create_employments(employment_entries: List[Dict]):
    """Create a collection of employment data classes

    """
    employments = []
    for entry in employment_entries:
        employments.append(Employment(**entry))
    return Employments(employment_entries=employments)


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


def create_skills(skill_entries: List[Dict]):
    """Create a collection of skill data classes

    """
    skills = []
    for entry in skill_entries:
        skills.append(Skill(**entry))
    return Skills(skill_entries=skills)


@dataclass
class Publication:
    """Publication data class

    """
    title: str
    authors: str
    date: str
    publication_name: str
    description: Optional[str] = None
