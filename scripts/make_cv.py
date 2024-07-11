"""Script to generate CV from personal data and job ad

"""
import typer

from src import (
    JobAdQualityExtractor,
    CVDataExtractionOrchestrator,
    JobAdsDAO,
    FormTemplatesTocDAO,
    get_anthropic_client,
    populate_html,
)

app = typer.Typer()


@app.command()
def main(
        job_ad_company: str = typer.Argument(..., help='Name of the company whose job ad to tailor CV to'),
        job_ad_title: str = typer.Argument(..., help='Name of position of job ad to tailor CV to'),
        cv_template: str = typer.Argument(..., help='Name of CV template to use'),
        person_name: str = typer.Argument(..., help='Name of person to generate CV for'),
        api_key_env: str = typer.Option('ANTHROPIC_API_KEY', "--api-key-env", help='Environment variable with API key'),
        verbosity: int = typer.Option(0, help='Verbosity level'),
):
    """Generate CV from personal data and job ad

    """
    typer.echo(f'Generating CV for {person_name} for position {job_ad_title} at {job_ad_company} and CV template {cv_template}')

    # Get the Anthropic client
    anthropic_client = get_anthropic_client(api_key_env)

    # Step 1: Extract key qualities and attributes from job ad
    ad_qualities = JobAdQualityExtractor(
        client=anthropic_client,
    ).extract_qualities(
        text=JobAdsDAO().get(job_ad_company, job_ad_title),
    )

    # Step 2: Ascertain the data sections required by the CV template and collect the data
    cv_data_orchestrator = CVDataExtractionOrchestrator(
        client=anthropic_client,
        relevant_qualities=ad_qualities,
        n_words=200,
    )
    template_required_cv_data = FormTemplatesTocDAO().get(cv_template, 'required_cv_data_types')
    cv_data = {}
    for required_cv_data in template_required_cv_data:
        cv_data.update(cv_data_orchestrator.run(
            cv_data_type=required_cv_data,
            data_key=person_name
        ))

    # Step 3: Render the CV with data and template
    html = populate_html(
        template_name=cv_template,
        cv_data=list(cv_data.values()),
    )
    print (html)


if __name__ == '__main__':
    main('epic resolution index',
         'luxury retail lighting specialist',
         'single_column_0',
         'gregor samsa',
         'ANTHROPIC_API_KEY',
         )
