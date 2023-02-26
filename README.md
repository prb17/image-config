[![ubuntue-dev](https://github.com/prb17/image-config/actions/workflows/ubuntu-dev-deploy.yml/badge.svg)](https://github.com/prb17/image-config/actions/workflows/ubuntu-dev-deploy.yml)

# image-config
Repo designed to configure Dockerfiles based on specific needs

## images hosted here:

- `ubuntu-dev`

## configuring a Docker file
#### seeing available parameters
```
./configure.py --help
```

#### explanation of parameters

- --config-image: a supported config file present in the `config` directory. 
    - Example: `ubuntu-dev` 
    - REQUIRED: yes
- --output-dir: the location to where the generated Dockerfile will be saved to. 
    - Example: `/tmp` `note`: directory must already exist
    - REQURED: no
    - DEFAULT=`.`
- --log-level: the desired logging level. `debug` presents detailed info whereas `info` has more basic logs. 
    - Example: `debug`
    - REQUIRED: no
    - DEFAULT=`info`

#### example command
```
./configure.py --config-image ubuntu-dev --output_dir ./tmp/ --log-level debug
```
This will configure an ubuntu-dev Dockerfile and save it to the ./tmp directory
