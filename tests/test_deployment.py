import copy
import glob
import json
import os
from string import Template

import dotenv
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


@pytest.fixture(scope="module")
def component_paths(root_dir):
    yield [path for loc in COMPONENT_LOCATIONS for path in glob.glob(os.path.join(root_dir, "birdhouse", loc, "*"))]


@pytest.fixture(scope="module")
def component_service_configs(component_paths):
    yield [
        os.path.join(component_path, "service-config.json.template")
        for component_path in component_paths
        if os.path.isfile(os.path.join(component_path, "service-config.json.template"))
    ]


@pytest.fixture(scope="module")
def template_substitutions(component_paths):
    templates = {}
    for component in component_paths:
        component_default = os.path.join(component, "default.env")
        if os.path.isfile(component_default):
            templates.update(dotenv.dotenv_values(component_default))
    templates.update(TEMPLATE_SUBSTITUTIONS)
    return templates


@pytest.fixture(scope="module", params=[pytest.lazy_fixture("component_service_configs")])
def resolved_services_config_schema(request):
    """
    For each of the services provided by ``component_paths`` fixture, obtain the referenced ``$schema``.

    If variable ``DACCS_NODE_REGISTRY_BRANCH`` is defined, the referenced ``$schema`` is ignored in favor of it.
    """
    service_config_paths = request.param
    assert service_config_paths, "Invalid service configuration. No service config found."

    # test override
    branch = os.environ.get("DACCS_NODE_REGISTRY_BRANCH", None)
    default_schema = {
        "$ref": "https://raw.githubusercontent.com/DACCS-Climate/Marble-node-registry"
                f"/{branch or 'main'}/node_registry.schema.json#service"
    }
    if branch:
        return [(default_schema, path) for path in service_config_paths]

    else:
        service_config_schemas = []
        for config_path in service_config_paths:
            with open(config_path, mode="r", encoding="utf-8") as config_file:
                config_data = json.load(config_file)
            if isinstance(config_data, dict):
                config_data = [config_data]
            for config_item in config_data:
                config_schema = config_item.get("$schema", None)
                config_schema = config_schema or default_schema
                config_schema = {"$ref": config_schema}
                service_config_schemas.append((config_schema, config_path))
        return service_config_schemas


class TestDockerCompose:
    def test_service_config_name_same_as_dirname(self, component_service_configs, template_substitutions):
        invalid_names = []

        for service_config_file in component_service_configs:

            with open(service_config_file) as f:
                config_info = Template(f.read()).safe_substitute(template_substitutions)
                service_config_json = "[{}]".format(config_info) if config_info.strip().startswith("{") else config_info
                service_configs = json.loads(service_config_json)
            invalid_config_names = []
            for service_config in service_configs:
                config_name = service_config.get("name")
                path_name = os.path.basename(os.path.dirname(service_config_file))
                if config_name == path_name:
                    # If at least one service_config in the file contains a matching name, that's ok
                    break
                invalid_config_names.append((config_name, path_name))
            else:
                invalid_names.extend(invalid_config_names)
        assert not invalid_names, "service names in service-config.json.template should match the directory name"

    @pytest.mark.online
    def test_service_config_valid(self, resolved_services_config_schema, template_substitutions):
        invalid_schemas = []
        for service_config_schema, service_config_path in resolved_services_config_schema:
            with open(service_config_path) as f:
                config_info = Template(f.read()).safe_substitute(template_substitutions)
                service_config_json = "[{}]".format(config_info) if config_info.strip().startswith("{") else config_info
                service_configs = json.loads(service_config_json)
            for service_config in service_configs:
                try:
                    jsonschema.validate(instance=service_config, schema=service_config_schema)
                except jsonschema.exceptions.ValidationError as e:
                    invalid_schemas.append(f"{service_config_path} contains invalid service configuration: {e}")
        assert not invalid_schemas, "\n".join(invalid_schemas)
