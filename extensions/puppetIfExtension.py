from jinja2 import nodes
from jinja2.ext import Extension
import logging
from logging import info, warning, debug, error


class puppetIfExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['pif'])

    def __init__(self, environment):
        super().__init__(environment)
        logging.info(f"--------------------Initializing custom extension for tags {puppetIfExtension.tags}")

    def parse(self, parser):
        logging.info("getting lineno")
        lineno = next(parser.stream).lineno
        logging.info(f"line no ended up being {lineno}")

        # now we parse a single expression that is used as cache key.
        args = [parser.parse_expression()]
        logging.info(f"the args parsed from expression {args}")

        body = parser.parse_statements(["name:end"], drop_needle=True)
        logging.info(f"the body parsed from statements is: {body}")
        test = args[0]
        return nodes.If(test, body, [], []).set_lineno(lineno)