from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IInMinisite(IThemeSpecific):
    """Marker interface set on request after traversal in a minisite.
    """


class IMinisiteConfig(Interface):
    """Minisite data"""
