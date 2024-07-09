"""Script to generate CV from personal data and job ad

"""
import typer

from src import (
    JobAdQualityExtractor,
    EducationExtractor,
    register_persons,
    register_job_ads,
    get_anthropic_client,
)

app = typer.Typer()


@app.command()
def main(
        job_ad_company: str = typer.Argument(..., help='Name of the company whose job ad to tailor CV to'),
        job_ad_title: str = typer.Argument(..., help='Name of position of job ad to tailor CV to'),
        cv_template: str = typer.Argument(..., help='Name of CV template to use'),
        person_name: str = typer.Argument(..., help='Name of person to generate CV for'),
        api_key_env: str = typer.Option('ANTHROPIC_API_KEY', help='Environment variable with API key'),
        verbosity: int = typer.Option(0, help='Verbosity level'),
):
    """Generate CV from personal data and job ad

    """
    typer.echo(f'Generating CV for {person_name} for position {job_ad_title} at {job_ad_company} and CV template {cv_template}')

    # Get the Anthropic client
    anthropic_client = get_anthropic_client(api_key_env)

    # Step 1: Extract key qualities and attributes from job ad
    ad_qualities = JobAdQualityExtractor(
        client=anthropic_client
    ).extract_qualities(
        text=register_job_ads.get(job_ad_company, job_ad_title)
    )

    # Step 2: Extract and summarize educational background in light of job ad
    eds = EducationExtractor(
        client=anthropic_client,
        relevant_qualities=ad_qualities,
        n_words=100
    ).extract_education(
        text=register_persons.get(person_name, 'education')
    )
    print (eds)


if __name__ == '__main__':
    main('epic_resolution_index', 'luxury_retail_lighting_specialist', 'cv_0_template', 'george samsa')
