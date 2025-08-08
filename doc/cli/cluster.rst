Cluster CLI
===========

This page documents the CLI commands for managing HyperPod clusters.

Cluster Information Commands
----------------------------

List Clusters
~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.cluster:list_cluster
   :prog: hyp list-cluster
   :show-nested:

Cluster Context Commands
------------------------

Set Cluster Context
~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.cluster:set_cluster_context
   :prog: hyp set-cluster-context
   :show-nested:

Get Cluster Context
~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.cluster:get_cluster_context
   :prog: hyp get-cluster-context
   :show-nested:

Monitoring Commands
-------------------

Get Monitoring Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.cluster:get_monitoring
   :prog: hyp get-monitoring
   :show-nested: