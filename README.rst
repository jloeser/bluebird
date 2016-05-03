========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/bluebird/badge/?style=flat
    :target: https://readthedocs.org/projects/bluebird
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jloeser/bluebird.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jloeser/bluebird

.. |version| image:: https://img.shields.io/pypi/v/bluebird.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/bluebird

.. |downloads| image:: https://img.shields.io/pypi/dm/bluebird.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/bluebird

.. |wheel| image:: https://img.shields.io/pypi/wheel/bluebird.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/bluebird

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/bluebird.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/bluebird

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/bluebird.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/bluebird


.. end-badges

Bluebird - Redfish for libvirt.

* Free software: BSD license

Installation
============

::

    pip install bluebird

Documentation
=============

https://bluebird.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
