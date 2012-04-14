# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory
from zope.interface import Invalid

Click2SellMessageFactory = MessageFactory('niteoweb.click2sell')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


def parse_mapping(mapping):
    """Iterate over mapping and check that it can be sucessfully parsed.

    Ignore empty lines.

    :param mappings: List of pipe-delimited mappings in
        ``<product_id>|<group_id>`` format.
    :type mappings: list

    :rtype: dict
    :return: product_ids as keys, group_names as values

    >>> from niteoweb.click2sell import parse_mapping

    Test formatting of a list of valid mappings
    >>> parse_mapping(['1|basic-members', '2|premium-members'])
    {'1': 'basic-members', '2': 'premium-members'}

    Test empty line is ignored
    >>> parse_mapping(['1|foobar', '  '])
    {'1': 'foobar'}

    Test formatting error
    >>> parse_mapping(['foo|bar|baz'])
    Traceback (most recent call last):
    ...
    Invalid: mapping 1 is not correctly formatted: foo|bar|baz
    """
    result = {}

    if not mapping:
        return {}

    for index, mapping in enumerate(mapping):
        try:
            # skip empty lines
            if not mapping.strip():
                continue

            # split line and trim whitespace
            product_id, group_name = mapping.split("|")
            product_id.strip()
            group_name.strip()

            # save in dict
            result[product_id] = group_name

        except:
            raise Invalid(
                "mapping {0} is not correctly formatted: {1}".format(
                    index + 1,
                    mapping,
                )
            )
    return result
