from zope.interface import implements

from cpskin.minisite.interfaces import IMinisite


class Minisite(object):

    implements(IMinisite)

    def __init__(self, main_portal_url, minisite_url, search_path):
        self.main_portal_url = main_portal_url
        self.minisite_url = minisite_url
        self.search_path = search_path
