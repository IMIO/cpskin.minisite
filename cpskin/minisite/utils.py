# -*- coding: utf-8 -*-
from cpskin.minisite.interfaces import IMinisiteConfig
from plone import api
from zope.component import getUtilitiesFor


def get_minisite_object(request):
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return None
    return api.content.get(minisite.search_path)


def get_minisite_navigation_level(minisite_obj):
    portal = api.portal.get()
    portal_physical_path = portal.getPhysicalPath()
    minisite_physical_path = minisite_obj.getPhysicalPath()
    minisite_path = [elem for elem in list(minisite_physical_path) if elem not in list(portal_physical_path)]  # noqa
    return len(minisite_path)


def list_minisites(portal):
    portal_path = '/'.join(portal.getPhysicalPath())
    configs = getUtilitiesFor(IMinisiteConfig, portal)
    result = [
        config for name, config in configs
        if config.search_path.startswith(portal_path)
    ]
    return result
