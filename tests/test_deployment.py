import os
import pytest
import glob
import json
from string import Template

import jsonschema

COMPONENT_LOCATIONS = ("core", "data", "services", "extensions", "test-helpers")
TEMPLATE_SUBSTITUTIONS = {"PAVICS_FQDN_PUBLIC": os.environ.get("PAVICS_FQDN_PUBLIC", "example.com")}


@pytest.fixture(scope="module")
def root_dir(request):
    yield os.path.dirname(os.path.dirname(request.fspath))


@pytest.fixture
def component_paths(root_dir):
    yield [path for loc in COMPONENT_LOCATIONS for path in glob.glob(os.path.join(root_dir, "birdhouse", loc, "*"))]


@pytest.fixture(scope="module")
def services_config_schema(request):
    with open(os.path.join(os.path.dirname(request.fspath), "service-config-schema.json")) as f:
        return json.load(f)


class TestDockerCompose:
    def test_service_config_name_same_as_dirname(self, component_paths):
        invalid_names = []

        for path in component_paths:
            service_config_file = os.path.join(path, "service-config.json.template")
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    service_config = json.loads(Template(f.read()).substitute(TEMPLATE_SUBSTITUTIONS))
                config_name = service_config.get("name")
                path_name = os.path.basename(path)
                if config_name != path_name:
                    invalid_names.append((config_name, path_name))
        assert not invalid_names, "service names in service-config.json.template should match the directory name"

    def test_service_config_valid(self, component_paths, services_config_schema):
        invalid_schemas = []

        for path in component_paths:
            service_config_file = os.path.join(path, "service-config.json.template")
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    service_config = json.loads(Template(f.read()).substitute(TEMPLATE_SUBSTITUTIONS))
                try:
                    jsonschema.validate(instance=service_config, schema=services_config_schema)
                except jsonschema.exceptions.ValidationError as e:
                    invalid_schemas.append(f"{os.path.basename(path)} contains invalid service configuration: {e}")
        assert not invalid_schemas, "\n".join(invalid_schemas)
