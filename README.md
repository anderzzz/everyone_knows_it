# Everyone Knows It

Tutorial code for a simple agentic workflow that generates content, layout and style of a CV.

The written tutorial is available at [at Towards Data Science](https://medium.com/towards-data-science/ai-write-and-style-my-cv-fb3168a5b10e) (no paywall).

## Getting Started
The main script is `make_cv.py` in `scripts/` folder. It performs the three main steps of the generation:
1. Extract key qualities of a job ad.
2. Orchestrate the generation of CV content sections given the CV template.
3. Render the content sections into a CV document given the CV template.

Of these steps the second is the most involved.

Data for illustration purposes are available in the `abtDataStore`, `formTemplatesStore` and `jobAdsStore` folders. With modifications to the data access objects in `src/dao.py` other data sources can be used.

## Source Code Outline
The fundamental agents that performs the generation are in `src/agent_base.py`. There are two kinds presently: one that sends and receive text from an LLM, no memory or tools; another that uses tools and returns the tool output.

The fundamental agents are instantiated in `src/agents.py` where agents that are specific for certain types of CV data are defined. This is also where the instruction prompt is assembled.

The orchestration of the agents with the raw data they process takes place in `src/orchestrator.py`. This is also where the association between CV data type of raw data DAOs are encoded, presently hard coded, but that could be changed to a configuration file.

The data classes are defined in `src/cv_data.py` and their associated builder functions too. The tools configurations for the CV data builders are in `src/confs/tools_confs/cv_data.json`.

The instruction prompt templates are jinja templates and rendered when agents are instantiated. The templates are in `src/prompt_templates`. Note that the files have to be named as the agent class name.

## CV Template Creation Prompts
The CV templates are created with the aid of Claude chatbot. The prompts used for the basic CV template creations, along with a crude drawing of the layout, are stored in the `template_creation_prompt` folder. These were used with Sonnet-3.5 to create the templates in the `formTemplatesStore` folder.
