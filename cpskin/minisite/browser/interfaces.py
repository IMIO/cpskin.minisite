from zope import schema
from zope.interface import Interface


class IHNavigationActivationView(Interface):
    """ media activation """

    can_enable_hnavigation = schema.Bool(
        u'Can enable multimedia viewlet',
        readonly=True
    )

    can_disable_hnavigation = schema.Bool(
        u'Can disable multimedia viewlet',
        readonly=True
    )

    def enable_hnavigation():
        """ Enable multimedia viewlet
        """

    def disable_hnavigation():
        """ Disable multimedia viewlet
        """


class IHNavigationActivated(Interface):
    """
    marker interface to tell if Horizontal Navigation is activate
    """
