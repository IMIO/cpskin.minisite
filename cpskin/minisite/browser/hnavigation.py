# -*- coding: utf-8 -*-
from cpskin.minisite.browser.interfaces import (IHNavigationActivated,
                                                IHNavigationActivationView
                                                )
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides
from cpskin.minisite.minisite import Minisite


class MSHorizontalNavigation(BrowserView):
    """
    Media activation helper view
    """
    implements(IHNavigationActivationView)

    def _redirect(self, msg=''):
        if self.request:
            if msg:
                api.portal.show_message(message=msg,
                                        request=self.request,
                                        type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    @property
    def is_in_minisite_mode(self):
        minisite = self.request.get('cpskin_minisite', None)
        if not isinstance(minisite, Minisite):
            return
        if minisite.is_in_minisite_mode:
            return True
        else:
            return False

    @property
    def can_enable_hnavigation(self):
        context = self.context
        return self.is_in_minisite_mode and not (IHNavigationActivated.providedBy(context))

    @property
    def can_disable_hnavigation(self):
        context = self.context
        return self.is_in_minisite_mode and (IHNavigationActivated.providedBy(context))

    def enable_hnavigation(self):
        import ipdb;ipdb.set_trace()
        context = self.context
        alsoProvides(context, IHNavigationActivated)
        self._redirect((u'Minisite horizontal Navigation enabled on content'))

    def disable_hnavigation(self):
        context = self.context
        noLongerProvides(context, IHNavigationActivated)
        self._redirect((u'Minisite horizontal Navigation disabled on content'))
