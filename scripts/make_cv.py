"""Script to generate CV from personal data and job ad

"""
import typer

from src import (
    JobAdQualityExtractor,
    CVDataExtractionOrchestrator,
    registry_persons,
    registry_job_ads,
    registry_form_templates,
    registry_form_templates_toc,
    get_anthropic_client,
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
        text=registry_job_ads.get(job_ad_company, job_ad_title)
    )

    # Step 2: Ascertain the data sections required by the CV template and collect the data
    cv_data_orchestrator = CVDataExtractionOrchestrator(
        client=anthropic_client,
        data_getter=registry_persons.get,
        relevant_qualities=ad_qualities,
        n_words=200,
    )
    for required_cv_data in registry_form_templates_toc.get(cv_template)['required_cv_data_types']:
        cv_data = cv_data_orchestrator.run(
            cv_data_type=required_cv_data,
            data_key=person_name
        )

#    # Step 3: Render the CV with data and template
#    html = make_html_from_template(
#        style_template=register_form_templates.get(cv_template),
#        data=cv_data
#    )


if __name__ == '__main__':
    main('epic resolution index',
         'luxury retail lighting specialist',
         'two_columns_0',
         'gregor samsa',
         'ANTHROPIC_API_KEY',
         )
