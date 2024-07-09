"""Creation of HTML files based on formTemplateStore and data

"""
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('formTemplateStore'))
template = env.get_template('test_template.html')

