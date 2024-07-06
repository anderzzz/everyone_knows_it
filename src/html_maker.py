"""Creation of HTML files based on templates and data

"""
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('test_template.html')

