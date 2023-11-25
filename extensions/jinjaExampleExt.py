from jinja2 import nodes
from jinja2.ext import Extension
import logging
from logging import info, warning, debug, error


class FragmentCacheExtension(Extension):
    # a set of names that trigger the extension.
    identifier = {"if"}
    tags = {"if"}

    def __init__(self, environment):
        super().__init__(environment)
        logging.info(f"--------------------Initializing custom extension for tags {FragmentCacheExtension.tags}")

        # add the defaults to the environment
        environment.extend(fragment_cache_prefix="", fragment_cache=None)

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        logging.info("getting lineno")
        lineno = next(parser.stream).lineno
        logging.info(f"line no ended up being {lineno}")

        # now we parse a single expression that is used as cache key.
        args = [parser.parse_expression()]
        logging.info(f"the args parsed from expression {args}")

        # if there is a comma, the user provided a timeout.  If not use
        # None as second parameter.
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(["name:end"], drop_needle=True)
        logging.info(f"the body that is parsed {body}")

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(
            self.call_method("_cache_support", args), [], [], body
        ).set_lineno(lineno)

    def _cache_support(self, name, timeout, caller):
        """Helper callback."""
        key = self.environment.fragment_cache_prefix + "name"

        # try to load the block from the cache
        # if there is no fragment in the cache, render it and store
        # it in the cache.
        rv = self.environment.fragment_cache.get(key)
        if rv is not None:
            return rv
        rv = caller()
        self.environment.fragment_cache.add(key, rv, timeout)
        return rv