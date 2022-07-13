#!/usr/bin/python3


from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import argparse
import logging
from logging import info, warning, debug, error

#define dict of configurable images and their corresponding template file
configurable_images = {'ubuntu-dev': 'Dockerfile.jinja', 'rhel-dev': 'Dockerfile.jinja'}

#logging dict
log_values = {'info': logging.INFO, 'warning': logging.WARN, 'debug': logging.DEBUG, 'error': logging.ERROR}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-image', required=True, choices=list(configurable_images.keys()), help='Desired image to configure')
    parser.add_argument("--output_dir", help="desired location for the generated Dockerfile. Default is this current directory", default="./")
    parser.add_argument("--log-level", choices=list(log_values.keys()), help="desired level of logging", default="info")
    args = parser.parse_args()
    return args

def main():
    prog_args = get_args()
    logging.basicConfig(format="{asctime} [{levelname}] {message}", style='{', level=log_values[prog_args.log_level])


    logging.info("setting up jinja environment")
    env = Environment (
        loader=PackageLoader("__main__"),
        autoescape=select_autoescape()
    )
    

    config_image = str(prog_args.config_image)
    logging.info(f'getting template information for image: \'{config_image}\'')
    template_file = configurable_images[config_image]
    logging.debug(f'using template: \'{template_file}\'')
    # looks automatically in './templates' directory
    template = env.get_template(template_file)


    logging.info("associating config image with the right config file")
    config_file = "config/" + prog_args.config_image + ".yml"
    logging.debug(f'picking config file: \'{config_file}\'')


    logging.info("opening the config file for reading")
    with open(config_file) as config_yaml:
        config = yaml.safe_load(config_yaml)
        logging.debug(f'the contents of the config file: \'{config}\'')
    

    logging.info("rendering the docker file content based on the configuration values")
    dockerfile_contents = template.render(config)
    logging.debug(f'What will be written to the Dockerfile:\n\'{dockerfile_contents}\'\n')

    logging.info("saving configured template to Dockerfile")
    output_file = prog_args.output_dir + 'Dockerfile'
    with open(output_file, 'w') as file:
        file.write(dockerfile_contents + "\n")
    logging.debug(f'Dockerfile saved to: \'{output_file}\'')

    logging.info("Done")

if __name__ == "__main__":
    main()
