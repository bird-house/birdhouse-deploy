import glob
import json
import os
from string import Template

import jsonschema
import pytest

COMPONENT_LOCATIONS = ("components", "optional-components", "config")
TEMPLATE_SUBSTITUTIONS = {
    "PAVICS_FQDN_PUBLIC": os.environ.get("PAVICS_FQDN_PUBLIC", "example.com"),
    "WEAVER_MANAGER_NAME": os.environ.get("WEAVER_MANAGER_NAME", "weaver"),
    "TWITCHER_PROTECTED_PATH": os.environ.get("TWITCHER_PROTECTED_PATH", "/twitcher/ows/proxy"),
}


@pytest.fixture(scope="module")
def root_dir(request):
    yield os.path.dirname(os.path.dirname(request.fspath))


@pytest.fixture
def component_paths(root_dir):
    yield [path for loc in COMPONENT_LOCATIONS for path in glob.glob(os.path.join(root_dir, "birdhouse", loc, "*"))]


@pytest.fixture(scope="module")
def services_config_schema():
    branch = os.environ.get("DACCS_NODE_REGISTRY_BRANCH", "main")
    schema = {
        "$ref": "https://raw.githubusercontent.com/DACCS-Climate/Marble-node-registry"
        f"/{branch}/node_registry.schema.json#service"
    }
    return schema


class TestDockerCompose:
    def test_service_config_name_same_as_dirname(self, component_paths):
        invalid_names = []

        for path in component_paths:
            service_config_file = os.path.join(path, "service-config.json.template")
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    config_info = Template(f.read()).safe_substitute(TEMPLATE_SUBSTITUTIONS)
                    service_configs = json.loads("[{}]".format(config_info))
                invalid_config_names = []
                for service_config in service_configs:
                    config_name = service_config.get("name")
                    path_name = os.path.basename(path)
                    if config_name == path_name:
                        # If at least one service_config in the file contains a matching name, that's ok
                        break
                    invalid_config_names.append((config_name, path_name))
                else:
                    invalid_names.extend(invalid_config_names)
        assert not invalid_names, "service names in service-config.json.template should match the directory name"

    @pytest.mark.online
    def test_service_config_valid(self, component_paths, services_config_schema):
        invalid_schemas = []

        for path in component_paths:
            service_config_file = os.path.join(path, "service-config.json.template")
            if os.path.isfile(service_config_file):
                with open(service_config_file) as f:
                    config_info = Template(f.read()).safe_substitute(TEMPLATE_SUBSTITUTIONS)
                    service_configs = json.loads("[{}]".format(config_info))
                for service_config in service_configs:
                    try:
                        jsonschema.validate(instance=service_config, schema=services_config_schema)
                    except jsonschema.exceptions.ValidationError as e:
                        invalid_schemas.append(f"{os.path.basename(path)} contains invalid service configuration: {e}")
        assert not invalid_schemas, "\n".join(invalid_schemas)
