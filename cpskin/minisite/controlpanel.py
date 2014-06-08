from zope.component import getUtilitiesFor
from Products.Five.browser import BrowserView

from cpskin.minisite.interfaces import IMinisiteConfig


class MinisitesPanel(BrowserView):

    def minisites(self):
        portal_url = self.context.absolute_url()
        configs = getUtilitiesFor(IMinisiteConfig, self.context)
        for name, config in configs:
            if portal_url.startswith(config.main_portal_url):
                yield config
