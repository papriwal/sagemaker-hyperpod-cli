import pytest
import json
import click
from click.testing import CliRunner
from unittest.mock import Mock, patch

from sagemaker.hyperpod.cli.inference_utils import load_schema_for_version, generate_click_command


class TestLoadSchemaForVersion:
    @patch('sagemaker.hyperpod.cli.inference_utils.pkgutil.get_data')
    def test_success(self, mock_get_data):
        data = {"properties": {"x": {"type": "string"}}}
        mock_get_data.return_value = json.dumps(data).encode()
        result = load_schema_for_version('1.2', 'pkg')
        assert result == data
        mock_get_data.assert_called_once_with('pkg.v1_2', 'schema.json')

    @patch('sagemaker.hyperpod.cli.inference_utils.pkgutil.get_data')
    def test_not_found(self, mock_get_data):
        mock_get_data.return_value = None
        with pytest.raises(click.ClickException) as exc:
            load_schema_for_version('3.0', 'mypkg')
        assert "Could not load schema.json for version 3.0" in str(exc.value)

    @patch('sagemaker.hyperpod.cli.inference_utils.pkgutil.get_data')
    def test_invalid_json(self, mock_get_data):
        mock_get_data.return_value = b'invalid'
        with pytest.raises(json.JSONDecodeError):
            load_schema_for_version('1.0', 'pkg')


class TestGenerateClickCommand:
    def setup_method(self):
        self.runner = CliRunner()

    def test_registry_required(self):
        with pytest.raises(ValueError):
            generate_click_command()

    @patch('sagemaker.hyperpod.cli.inference_utils.load_schema_for_version')
    def test_unsupported_version(self, mock_load_schema):
        mock_load_schema.return_value = {'properties': {}, 'required': []}
        # Registry missing the default version key
        registry = {}

        @click.command()
        @generate_click_command(registry=registry)
        def cmd(namespace, version, domain):
            click.echo('should not')

        # Invocation with no args uses default version 1.0 which is unsupported
        res = self.runner.invoke(cmd, [])
        assert res.exit_code != 0
        assert 'Unsupported schema version: 1.0' in res.output

    @patch('sagemaker.hyperpod.cli.inference_utils.load_schema_for_version')
    def test_json_flags(self, mock_load_schema):
        mock_load_schema.return_value = {'properties': {}, 'required': []}
        # Domain receives flags as attributes env, dimensions, resources_limits, resources_requests
        class DummyFlat:
            def __init__(self, **kwargs): self.__dict__.update(kwargs)
            def to_domain(self): return self
        registry = {'1.0': DummyFlat}

        @click.command()
        @generate_click_command(registry=registry)
        def cmd(namespace, version, domain):
            click.echo(json.dumps({
                'env': domain.env, 'dimensions': domain.dimensions,
                'limits': domain.resources_limits, 'reqs': domain.resources_requests
            }))

        # valid JSON
        res_ok = self.runner.invoke(cmd, [
            '--env', '{"a":1}',
            '--dimensions', '{"b":2}',
            '--resources-limits', '{"c":3}',
            '--resources-requests', '{"d":4}'
        ])
        assert res_ok.exit_code == 0
        out = json.loads(res_ok.output)
        assert out == {'env': {'a':1}, 'dimensions': {'b':2}, 'limits': {'c':3}, 'reqs': {'d':4}}

        # invalid JSON produces click error
        res_err = self.runner.invoke(cmd, ['--env', 'notjson'])
        assert res_err.exit_code == 2
        assert 'must be valid JSON' in res_err.output

    @patch('sagemaker.hyperpod.cli.inference_utils.load_schema_for_version')
    def test_type_mapping_and_defaults(self, mock_load_schema):
        mock_load_schema.return_value = {
            'properties': {
                's': {'type': 'string'},
                'i': {'type': 'integer'},
                'n': {'type': 'number'},
                'b': {'type': 'boolean'},
                'e': {'type': 'string', 'enum': ['x','y']},
                'd': {'type': 'string', 'default': 'Z'}
            },
            'required': ['s']
        }
        class DummyFlat:
            def __init__(self, **kwargs): self.__dict__.update(kwargs)
            def to_domain(self): return self
        registry = {'1.0': DummyFlat}

        @click.command()
        @generate_click_command(registry=registry)
        def cmd(namespace, version, domain):
            click.echo(f"{domain.s},{domain.i},{domain.n},{domain.b},{domain.e},{domain.d}")

        res = self.runner.invoke(cmd, [
            '--s', 'hello', '--i', '5', '--n', '2.5', '--b', 'True', '--e', 'x'
        ])
        assert res.exit_code == 0
        assert res.output.strip() == 'hello,5,2.5,True,x,Z'

    @patch('sagemaker.hyperpod.cli.inference_utils.load_schema_for_version')
    def test_version_key_and_schema_pkg(self, mock_load_schema):
        mock_load_schema.return_value = {'properties': {}, 'required': []}
        class DummyFlat:
            def __init__(self, **kwargs): pass
            def to_domain(self): return self
        registry = {'v2': DummyFlat}

        @click.command()
        @generate_click_command(version_key='v2', schema_pkg='mypkg', registry=registry)
        def cmd(namespace, version, domain):
            click.echo(version)

        res = self.runner.invoke(cmd, [])
        assert res.exit_code == 0
        mock_load_schema.assert_called_once_with('v2', 'mypkg')
