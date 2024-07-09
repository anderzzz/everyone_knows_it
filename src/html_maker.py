"""Creation of HTML files based on formTemplatesStore and data

"""
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('formTemplatesStore'))
template = env.get_template('test_template.html')

