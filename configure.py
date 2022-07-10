from jinja2 import Environment, PackageLoader, select_autoescape
import yaml


def main():
    # setup the jinja environament
    env = Environment (
        loader=PackageLoader("__main__"),
        autoescape=select_autoescape()
    )
    template = env.get_template("Dockerfile.jinja")

    # grab the config values
    with open('config/baseUbuntu.yml') as config_yaml:
        config = yaml.safe_load(config_yaml)
        print(config)
    
    # render the docker file content based on the configuration values
    dockerfile_contents = template.render(config)
    print(dockerfile_contents)

    # write the newly configured content to the Dockerfile
    with open('Dockerfile', 'w') as output_file:
        output_file.write(dockerfile_contents + "\n")

if __name__ == "__main__":
    main()