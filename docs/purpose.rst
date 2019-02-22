Purpose
========================================

PyTan was created for a number of reasons:

#. To provide a way for Python programmers to work with the `Tanium <https://www.tanium.com>`_ API using native Python objects.
#. To provide workflow encapsulation for Python programmers that contains the order of steps it takes to do something. For each step in a workflow, a workflow knows what attributes need to be defined in a request, how to handle the response, and how the response should be passed on to the next step.
#. To provide a command line interface for non Python programmers that exposes the workflow encapsulation via a Python script that takes in arguments and options and passes them on to the underlying workflow.
