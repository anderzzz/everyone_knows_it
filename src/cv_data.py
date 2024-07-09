"""CV data classes

"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Union, Callable, Any


@dataclass
class Biography:
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
class Educations:
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
class Employments:
    """Collection of employment data classes

    """
    employment_entries: List[Employment]


@dataclass
class Skill:
    """Skill data class

    """
    name: str
    level: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Publication:
    """Publication data class

    """
    title: str
    authors: str
    date: str
    publication_name: str
    description: Optional[str] = None


class CVDataFactory:
    builders: Dict[str, Callable[..., Any]] = {
        'Biography': Biography,
        'Educations': create_educations,
    }

    @classmethod
    def create_cv_data(cls, data_type: str, data: List[Dict]):
        return cls.builders[data_type](data)
