Inference CLI
=============

This page documents the CLI commands for managing inference endpoints.

.. note::
   Create commands use dynamic parameter generation and are documented in the :doc:`../cli_reference` page.

Invoke Commands
---------------

Invoke Custom Endpoint
~~~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.inference:custom_invoke
   :prog: hyp invoke
   :show-nested:

List Commands
-------------

List Jumpstart Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.inference:js_list
   :prog: hyp list
   :show-nested:

List Custom Endpoints
~~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.inference:custom_list
   :prog: hyp list
   :show-nested:

Describe Commands
-----------------

Describe Jumpstart Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. click:: sagemaker.hyperpod.cli.commands.inference:js_describe
   :prog: hyp describe
   :show-nested: