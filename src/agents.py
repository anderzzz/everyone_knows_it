"""Extract key qualities and attributes from a job ad

"""
from agent_base import AgentBareMetal


class JobAdQualityExtractor:
    """Agent that extracts key qualities and attributes from a job ad

    """
    def __init__(self,
                 model: str = 'claude-3-haiku-20240307',
                 api_key: str = 'ANTHROPIC_API_KEY',
                 ):
        self.agent = AgentBareMetal(
            api_key=api_key,
            model=model,
            instruction="""
            Your task is to analyze a job ad and from it extract, on the one hand, the qualities and attributes that the company is looking for in a candidate, and on the other hand, the qualities and aspirations the company communicates about itself. 
            
            Any boilerplate text or contact information should be ignored. And where possible, reduce the overall amount of text. We are looking for the essence of the job ad.
            """,
        )

    def extract_qualities(self, text: str) -> str:
        return self.agent.run(text)
