from jinja2 import nodes
from jinja2.ext import Extension
import logging
from logging import info, warning, debug, error


class puppetHashExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['phash'])

    def __init__(self, environment):
        super().__init__(environment)
        logging.info(f"--------------------Initializing custom extension for tags {puppetHashExtension.tags}")

    def parse(self, parser):
        logging.info("getting lineno")
        lineno = next(parser.stream).lineno
        logging.info(f"line no ended up being {lineno}")

        args = [parser.parse_expression()]
        logging.info(f"the args parsed from expression {args}")

        more_args = [parser.parse_expression()]
        logging.info(f"the more_args parsed from expression {more_args}")

        body = parser.parse_statements(["name:end"], drop_needle=True)
        logging.info(f"the body parsed from statements is: {body}")
        
        return nodes.For(args[0], more_args[0], body, [], [], True).set_lineno(lineno)