"""Script to generate CV from personal data and job ad

"""
import typer


app = typer.Typer()


@app.command()
def main(
        job_ad: str = typer.Argument(..., help='Name of job ad to tailor CV to'),
        cv_template: str = typer.Argument(..., help='Name of CV template to use'),
        person_name: str = typer.Argument(..., help='Name of person to generate CV for'),
        verbosity: int = typer.Option(0, help='Verbosity level'),
):
    """Generate CV from personal data and job ad

    """
    typer.echo(f'Generating CV for {person_name} using job ad {job_ad} and CV template {cv_template}')

