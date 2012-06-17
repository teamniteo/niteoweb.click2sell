# -*- coding: utf-8 -*-
"""
Upgrade from version 0.3 to version 0.4
---------------------------------------
"""


def upgrade(context):
    """Upgrade steps from 0.3 to 0.4."""

    # update click2sell control panel configlet to point to a new URL that
    # renders from plone.app.registry records rather than from a local utility
    context.runImportStepFromProfile('profile-niteoweb.click2sell:default', 'controlpanel')

    # add click2sell records to plone.app.registry
    context.runImportStepFromProfile('profile-niteoweb.click2sell:default', 'plone.app.registry')

    # remove old click2sell persistent utility
    remove_persistent_utility(context)


def remove_persistent_utility(setup_tool):
    """Code taken from
    http://blog.fourdigits.nl/removing-a-persistent-local-utility-part-ii.
    """
    portal = setup_tool.getParentNode()
    sm = portal.getSiteManager()

    adapters = sm.utilities._adapters
    for x in adapters[0].keys():
        if x.__module__.find("niteoweb.click2sell") != -1:
            print "deleting %s" % x
            del adapters[0][x]
    sm.utilities._adapters = adapters

    subscribers = sm.utilities._subscribers
    for x in subscribers[0].keys():
        if x.__module__.find("niteoweb.click2sell") != -1:
            print "deleting %s" % x
            del subscribers[0][x]
    sm.utilities._subscribers = subscribers

    provided = sm.utilities._provided
    for x in provided.keys():
        if x.__module__.find("niteoweb.click2sell") != -1:
            print "deleting %s" % x
            del provided[x]
    sm.utilities._provided = provided

    for x in sm._utility_registrations.keys():
        if x[0].__name__ == 'IClick2SellSettings':
            print 'deleting IClick2SellSettings'
            del sm._utility_registrations[x]
