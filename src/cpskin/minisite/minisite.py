from zope.interface import implements

from cpskin.minisite.interfaces import IMinisite


class Minisite(object):

    implements(IMinisite)

    url = "http://minisite/url"
    searchpath = "search/path"
