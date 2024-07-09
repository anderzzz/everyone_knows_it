"""Script to generate CV from personal data and job ad

"""
import typer

from src import (
    JobAdQualityExtractor,
    EducationExtractor,
    register_persons,
    register_job_ads,
)

app = typer.Typer()


@app.command()
def main(
        job_ad_company: str = typer.Argument(..., help='Name of the company whose job ad to tailor CV to'),
        job_ad_title: str = typer.Argument(..., help='Name of position of job ad to tailor CV to'),
        cv_template: str = typer.Argument(..., help='Name of CV template to use'),
        person_name: str = typer.Argument(..., help='Name of person to generate CV for'),
        verbosity: int = typer.Option(0, help='Verbosity level'),
):
    """Generate CV from personal data and job ad

    """
    typer.echo(f'Generating CV for {person_name} for position {job_ad_title} at {job_ad_company} and CV template {cv_template}')

    ad_text = register_job_ads.get(job_ad_company, job_ad_title)
    ad_qualities = JobAdQualityExtractor().extract_qualities(ad_text)
    eds = EducationExtractor(
        relevant_qualities=ad_qualities,
        n_words=100
    ).extract_education(
        register_persons.get(person_name, 'education')
    )
    print (eds)


if __name__ == '__main__':
    main('epic_resolution_index', 'luxury_retail_lighting_specialist', 'cv_0_template', 'george samsa')
