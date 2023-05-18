import os
import pytest
import glob
import yaml
import json
from string import Template

import jsonschema

COMPONENT_LOCATIONS = ('core', 'data', 'services', 'extensions', 'test-helpers')
TEMPLATE_SUBSTITUTIONS = {'PAVICS_FQDN_PUBLIC': os.environ.get('PAVICS_FQDN_PUBLIC', 'example.com')}


@pytest.fixture(scope="module")
def root_dir(request):
    yield os.path.dirname(os.path.dirname(request.fspath))


@pytest.fixture
def component_paths(root_dir):
    yield [path for loc in COMPONENT_LOCATIONS for path in glob.glob(os.path.join(root_dir, 'birdhouse', loc, '*'))]


@pytest.fixture
def compose_paths(component_paths):
    return [compose for path in component_paths if os.path.isfile(compose := os.path.join(path, 'docker-compose-extra.yml'))]


@pytest.fixture(scope="module")
def services_config_schema(request):
    with open(os.path.join(os.path.dirname(request.fspath), 'service-config-schema.json')) as f:
        return json.load(f)


class TestDockerCompose:
    def test_no_exposed_ports(self, compose_paths):
        exceptions = ['proxy']
        exposed_ports = {}

        for compose_file in compose_paths:
            with open(compose_file) as f:
                yml = yaml.safe_load(f)
            for name, details in yml.get('services', {}).items():
                if name not in exceptions and details.get('ports'):
                    exposed_ports[name] = details.get('ports')
        assert not exposed_ports, 'no ports should be exposed except for the proxy container'

    @pytest.mark.skip
    def test_no_container_names(self, compose_paths):
        container_names = {}

        for compose_file in compose_paths:
            with open(compose_file) as f:
                yml = yaml.safe_load(f)
            for name, details in yml.get('services', {}).items():
                container_names[name] = details.get('container_name')
        assert not container_names, 'no containers should have an explicit container name'

    def test_service_name_same_as_dirname(self, compose_paths):
        exceptions = ['monitoring']
        mismatch_names = []

        for compose_file in compose_paths:
            dirname = os.path.basename(os.path.dirname(compose_file))
            if dirname in exceptions:
                continue
            with open(compose_file) as f:
                yml = yaml.safe_load(f)
            services = yml.get("services")
            if services and dirname not in services:
                mismatch_names.append(dirname)
        assert not mismatch_names, 'docker compose service names should match the directory basename'

    def test_service_config_name_same_as_dirname(self, component_paths):
        invalid_names = []

        for path in component_paths:
            service_config_file = os.path.join(path, 'service-config.json.template')
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    service_config = json.loads(Template(f.read()).substitute(TEMPLATE_SUBSTITUTIONS))
                config_name = service_config.get("name")
                path_name = os.path.basename(path)
                if config_name != path_name:
                    invalid_names.append((config_name, path_name))
        assert not invalid_names, 'service names in service-config.json.template should match the directory name'

    def test_service_config_valid(self, component_paths, services_config_schema):
        invalid_schemas = []

        for path in component_paths:
            service_config_file = os.path.join(path, 'service-config.json.template')
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    service_config = json.loads(Template(f.read()).substitute(TEMPLATE_SUBSTITUTIONS))
                try:
                    jsonschema.validate(instance=service_config, schema=services_config_schema)
                except jsonschema.exceptions.ValidationError as e:
                    invalid_schemas.append(f"{os.path.basename(path)} contains invalid service configuration: {e}")
        assert not invalid_schemas, '\n'.join(invalid_schemas)

    def test_logging(self, compose_paths):
        bad_logging = []
        good_logging_config = {"driver": "json-file", "options": {"max-size": "50m", "max-file": "10"}}
        for compose_file in compose_paths:
            with open(compose_file) as f:
                yml = yaml.safe_load(f)
            for name, details in yml.get('services', {}).items():
                logging_details = details.get('logging')
                if logging_details != good_logging_config:
                    bad_logging.append((name, logging_details))
        errors = '\n'.join(f"service: {name}, logging: '{config}'" for name, config in bad_logging)
        assert not bad_logging, f"services should all use the following logging configuration {good_logging_config}: errors: \n {errors}"
