#!/usr/bin/python3

from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import argparse
import logging
from logging import info, warning, debug, error
from extensions import puppetIfExtension, jinjaExampleExt, puppetHashExtension
from cachelib import SimpleCache
import re

#define dict of configurable images and their corresponding template file
configurable_images = {'hiera': './templates/file.erb.xml', 'rhel-dev': 'Dockerfile.jinja'}

#logging dict
log_values = {'info': logging.INFO, 'warning': logging.WARN, 'debug': logging.DEBUG, 'error': logging.ERROR}

class dict(dict):
    def __init__(self, *args):
        super().__init__(args)
        self.each = ["one", "two",]
        

class PuppetDict():
    def __init__(self):
        logging.info("Creating a puppet dict")
        self.each = {("one", "1"), ("two", "2")}

    def dig(self):
        logging.info("Calling the puppet dict dig function")
        return "Some string"

def each(iterable):
    if isinstance(iterable, list):
        return iterable
    elif isinstance(iterable, dict):
        return iterable.items()
    else:
        return []

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, choices=list(configurable_images.keys()), help='Desired image to configure')
    parser.add_argument("--output-dir", help="desired location for the generated Dockerfile. Default is this current directory", default="./")
    parser.add_argument("--log-level", choices=list(log_values.keys()), help="desired level of logging", default="info")
    args = parser.parse_args()
    return args

def format_hash(template_str):
    template_arr = template_str.splitlines()
    for idx,line in enumerate(template_arr):
        found = line.find("each do |")
        logging.info(f"Found: {found}")
        if found > -1:
            logging.info(f"Line {idx} in arr: {line}")
            line = line.replace("<%", "<% phash")
            line = line.replace(" do", "")
            segments = line.split()
            segments.insert(2, segments.pop(-2).replace("|",""))
            line = " ".join(segments)
            logging.info(f"Segments: {segments}")
            template_arr[idx] = line

    return "\n".join(template_arr)

def format_template(filename):
    with open(filename, 'r') as file:
        data = file.read()
    data = data.replace('@', '')
    data = data.replace("<% if ", "<% pif ")
    data = format_hash(data)
    # data = data.replace(".each", ".items()")
    # data = data.replace('|', '').replace(" do ", " for ")
    return data

def main():
    prog_args = get_args()
    logging.basicConfig(format="{asctime} [{levelname}] {message}", style='{', level=log_values[prog_args.log_level])


    logging.info("setting up jinja environment")
    env = Environment (
        loader=PackageLoader("puppet"),
        autoescape=select_autoescape(),
        extensions=[
            # jinjaExampleExt.FragmentCacheExtension, 
            puppetIfExtension.puppetIfExtension, 
            puppetHashExtension.puppetHashExtension
            ],
	    block_start_string="<%",
	    block_end_string="%>",
        variable_start_string="<%=",
        variable_end_string="%>"
    )
    env.filters['each'] = each
    # env.fragment_cache = SimpleCache()
    # env.compile_expression("do")
    

    config_image = str(prog_args.config)
    logging.info(f'getting template information for image: \'{config_image}\'')
    template_file = configurable_images[config_image]
    logging.debug(f'using template: \'{template_file}\'')
    # looks automatically in './templates' directory
    template_str = format_template(template_file)
    logging.info(f'template looks like: \n\'{template_str}\'')

    # template = env.parse(template_str)
    # logging.info(f"the template after parsing \n'{template}'")


    #--------------------------------------------
    template = env.from_string(template_str)
    logging.info(f"the template after parsing \n'{template}'")
    

    logging.info("associating config image with the right config file")
    config_file = "config/" + prog_args.config + ".yaml"
    logging.debug(f'picking config file: \'{config_file}\'')


    logging.info("opening the config file for reading")
    with open(config_file) as config_yaml:
        config = yaml.safe_load(config_yaml)    
    # config['pdict'] = PuppetDict()
    # config['restrict'] = dict()
    logging.debug(f'the contents of the config file: \'{config}\'')

    logging.info("rendering the docker file content based on the configuration values")
    dockerfile_contents = template.render(config)
    logging.debug(f'What will be written to the Dockerfile:\n\'{dockerfile_contents}\'\n')

    # logging.info("saving configured template to Dockerfile")
    # output_file = prog_args.output_dir + 'Dockerfile'
    # with open(output_file, 'w') as file:
    #     file.write(dockerfile_contents + "\n")
    # logging.debug(f'Dockerfile saved to: \'{output_file}\'')

    logging.info("Done")

if __name__ == "__main__":
    main()
