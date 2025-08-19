Training CLI
============

This page documents the CLI commands for managing PyTorch training jobs.

.. note::
   Create commands use dynamic parameter generation and are documented in the :doc:`../cli_training` page.

List Commands
-------------

List PyTorch Jobs
~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.training:list_jobs
   :prog: hyp list
   :show-nested:

Describe Commands
-----------------

Describe PyTorch Job
~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.training:pytorch_describe
   :prog: hyp describe
   :show-nested:

Delete Commands
---------------

Delete PyTorch Job
~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.training:pytorch_delete
   :prog: hyp delete
   :show-nested:

Pod Management Commands
-----------------------

List Job Pods
~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.training:pytorch_list_pods
   :prog: hyp list-pods
   :show-nested:

Get Pod Logs
~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.training:pytorch_get_logs
   :prog: hyp get-logs
   :show-nested: