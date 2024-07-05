"""The semantic flow logic

"""
import json

from agent import Agent
from drl import get_data


def main():
    with open(get_data('education')) as f:
        education_data = json.load(f)
    agent = Agent(
        api_key='ANTHROPIC_API_KEY',
        instruction="""You assist the user in writing a resume. The role is technical and you should keep the resume short with emphasis on technical accomplishments.
        
        The user will provide you with JSON data containing the raw data from which to compile relevant and brief resume information.
        Also note that the JSON data may contain references to `M3`, which should be replaced with the user's name, as provided by the user.
        """,
        tools=['Educations'],
    )
    text = 'The following JSON data contains the education information of "Anders Ohrn".\n\n' + json.dumps(education_data, indent=4)
    out = agent.run(text)
    print (out)


if __name__ == '__main__':
    main()