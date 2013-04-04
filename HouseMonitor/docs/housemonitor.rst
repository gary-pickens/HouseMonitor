housemonitor Package
====================

The house monitor package is a system for monitoring various inputs and reacting to those inputs.  It's operation is as follows:
1.  **Inputs** generally come in via a serial port from a xbee.  Each input is on it's own thread and feeds the main port of the
system via the input queue.
2.  **Steps**


:mod:`HouseMonitor` Module
--------------------------

.. automodule:: housemonitor.HouseMonitor
    :members:
    :undoc-members:
    :show-inheritance:

Subpackages
-----------

.. toctree::

    housemonitor.configuration
    housemonitor.hm
    housemonitor.inputs
    housemonitor.lib
    housemonitor.outputs
    housemonitor.steps

