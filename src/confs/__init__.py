import os

_conf_root_dir = os.path.dirname(os.path.abspath(__file__))

tools_cv_data = os.path.join(_conf_root_dir, 'tools_confs/cv_data.json')
tools_funcs = os.path.join(_conf_root_dir, 'tools_confs/funcs.json')

agent_model_extractor_conf = os.path.join(_conf_root_dir, 'agent_model_confs/extractors.json')
