from zope.interface import implements
from zope.interface import alsoProvides

from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.interfaces import IInMinisite
from cpskin.minisite.interfaces import IInPortal
from cpskin.minisite import logger


class MinisiteConfig(object):

    implements(IMinisiteConfig)

    def __init__(self, main_portal_url, minisite_url, search_path):
        self.main_portal_url = main_portal_url
        self.minisite_url = minisite_url
        self.search_path = search_path


def decorateRequest(request, config):
    minisite = request.get('cpskin_minisite', None)
    if isinstance(minisite, Minisite):
        return
    if config:
        minisite = Minisite(request, config)
        if minisite.is_in_minisite_mode:
            alsoProvides(request, IInMinisite)
        else:
            alsoProvides(request, IInPortal)
        logger.debug('Request at {} is marked as minisite'.format(request.URL))
    else:
        minisite = NotInMinisite()
    request.set('cpskin_minisite', minisite)


class NotInMinisite(object):

    is_minisite = False
    is_in_minisite_mode = False
    is_in_portal_mode = False
    main_portal_url = ''
    minisite_url = ''
    search_path = ''


class Minisite(object):

    is_minisite = True

    def __init__(self, request, config):
        self.main_portal_url = config.main_portal_url
        self.minisite_url = config.minisite_url
        self.search_path = config.search_path
        self.is_in_minisite_mode = request.URL.startswith(self.minisite_url)
        self.is_in_portal_mode = request.URL.startswith(self.main_portal_url)
