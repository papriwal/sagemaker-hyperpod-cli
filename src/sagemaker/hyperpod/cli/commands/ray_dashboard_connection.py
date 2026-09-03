# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import click
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from sagemaker.hyperpod.cli.constants.ray_dashboard_connection_constants import (
    RAY_DASHBOARD_CONNECTION_GROUP,
    RAY_DASHBOARD_CONNECTION_VERSION,
    RAY_DASHBOARD_CONNECTION_PLURAL,
)
from sagemaker.hyperpod.common.telemetry.telemetry_logging import (
    _hyperpod_telemetry_emitter,
)
from sagemaker.hyperpod.common.telemetry.constants import Feature
from sagemaker.hyperpod.common.cli_decorators import handle_cli_exceptions


def _load_kube_config():
    """Load kubeconfig so the default ApiClient is authenticated.

    Uses the library's default client (as HPSpace does) rather than copying
    the token out of Configuration.api_key. The api_key entry is named
    differently across kubernetes-client releases ("authorization" in 36.0.0,
    "BearerToken" in 36.0.3+), so reading it by name is version-fragile.
    """
    config.load_kube_config()


@click.command("ray-dashboard-connection")
@click.option("--cluster-name", required=True, help="Name of the RayCluster")
@click.option("--namespace", "-n", required=False, default="default", help="Namespace of the RayCluster")
@_hyperpod_telemetry_emitter(Feature.HYPERPOD_CLI, "create_ray_dashboard_connection")
@handle_cli_exceptions()
def create_ray_dashboard_connection(cluster_name, namespace):
    """Create a RayDashboardConnection to get a dashboard URL for a RayCluster."""
    _load_kube_config()

    body = {
        "apiVersion": f"{RAY_DASHBOARD_CONNECTION_GROUP}/{RAY_DASHBOARD_CONNECTION_VERSION}",
        "kind": "RayDashboardConnection",
        "metadata": {
            "namespace": namespace,
        },
        "spec": {
            "clusterName": cluster_name,
        },
    }

    api = client.CustomObjectsApi()

    try:
        result = api.create_namespaced_custom_object(
            group=RAY_DASHBOARD_CONNECTION_GROUP,
            version=RAY_DASHBOARD_CONNECTION_VERSION,
            namespace=namespace,
            plural=RAY_DASHBOARD_CONNECTION_PLURAL,
            body=body,
        )
    except ApiException as e:
        if e.status == 404:
            body_str = e.body or ""
            if "raydashboardconnections" in body_str.lower() or RAY_DASHBOARD_CONNECTION_GROUP in body_str:
                raise click.ClickException(
                    "The RayDashboardConnection API is not available on this cluster.\n"
                    "Please install the hyperpod-ray-endpoint-operator Helm chart.\n"
                )
            raise click.ClickException(f"Not found: {body_str}")
        raise

    connection_url = result.get("status", {}).get("connectionUrl", "")
    if connection_url:
        click.echo(connection_url)
    else:
        raise click.ClickException(
            f"Failed to get dashboard URL for RayCluster '{cluster_name}' in namespace '{namespace}'.\n"
            "Please contact your cluster administrator."
        )
