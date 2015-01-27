from zope.component import getUtilitiesFor
from Products.Five.browser import BrowserView

from cpskin.minisite.interfaces import IMinisiteConfig


class MinisitesPanel(BrowserView):

    def minisites(self):
        # import ipdb;ipdb.set_trace()        
        portal_path = '/'.join(self.context.getPhysicalPath())
        # ex : portal_path contient /enghien
        configs = getUtilitiesFor(IMinisiteConfig, self.context)
        # chaque config contenu dans name peuvent contenir par ex : /enghien/ma-ville/services-communaux/departement-administratif
        # config.filename = /home/zope/instances/enghien_site_433/var/instance1/minisites/enghien-un-mini-site.imio-test.be.ini
        # config.main_portal_url = http://enghien4.imio-test.be'
        # config.minisite_url = http://enghien-un-mini-site.imio-test.be
        # config.obj
        # config.search_path = /enghien/ma-ville/services-communaux/departement-administratif
        result = [
            config for name, config in configs
            if config.search_path.startswith(portal_path)
        ]
        return result
