# python-apt-wheel
Ansible playbooks to build wheel files for python-apt

## Goals

This project aims to give people the ability to build python wheel files for python-apt to allow installation in virtual environments without using `--system-site-packages`

## Use

### Requirements

1. Have access to docker, either installed locally or available and configured via `DOCKER_` environment variables
2. Ansible >= 2.3

### Executing

```
$ ansible-playbook -i hosts -v python-apt.yml
```

Wheel files will be downloaded into the `wheelhouse` directory.

## debian_control_file

This is a custom Ansible module that parses a debian packaging control file and provides information from all package paragraphs

## docker.pex?

To avoid needing to install `docker-py` to work with the Ansible `docker_container` module, a PEX file with `docker-py` installed within is provided to work as the `ansible_python_interpreter` for `docker_container` tasks.

To read more about PEX check out [https://pex.readthedocs.io/en/stable/](https://pex.readthedocs.io/en/stable/)
