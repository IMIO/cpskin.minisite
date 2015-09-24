from zope.interface import implements
from Acquisition import aq_base, aq_parent, aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationTabs
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase
from plone import api

from cpskin.minisite.browser.interfaces import IHNavigationActivated
from cpskin.locales import CPSkinMessageFactory as _

from cpskin.minisite.minisite import Minisite
HAS_MENU = False
try:
    from cpskin.menu.interfaces import IFourthLevelNavigation
    HAS_MENU = True
except ImportError:
    pass


class MinisiteViewlet(ViewletBase):
    index = ViewPageTemplateFile('minisite_in_minisite.pt')

    def url_in_portal_mode(self):
        portal_url = getToolByName(self.context, 'portal_url')
        relative_url = portal_url.getRelativeContentURL(self.context)
        portal = portal_url.getPortalObject()
        main_portal_url = self.request.cpskin_minisite.main_portal_url
        minisite_url = self.request.cpskin_minisite.minisite_url
        root_url = portal.absolute_url()
        root_url_in_portal_mode = root_url.replace(
            minisite_url,
            main_portal_url
        )
        return '/'.join((root_url_in_portal_mode, relative_url))


class SearchBoxViewlet(SearchBoxBase):
    index = ViewPageTemplateFile('searchbox_in_minisite.pt')


def calculate_top_level(context):
    """Calculate top level of navigation menu to take care of 4th level menu
    NB : IFourthLevelNavigation is activated on the third level folder
    """
    portal = api.portal.get()
    contextPhyPath = context.getPhysicalPath()
    portalPhyPath = portal.getPhysicalPath()
    path = [elem for elem in list(contextPhyPath) if elem not in list(portalPhyPath)]
    depth = len(path)
    if depth >= 3:
        subLevels = depth - 3
        if subLevels:
            thirdLevelPath = '/'.join(contextPhyPath[:-subLevels])
        else:
            thirdLevelPath = '/'.join(contextPhyPath)
        thirdLevelFolder = portal.unrestrictedTraverse(thirdLevelPath)
        if HAS_MENU:
            if IFourthLevelNavigation.providedBy(thirdLevelFolder):
                return 4
    return depth


class MinisiteCatalogNavigationTabs(CatalogNavigationTabs):
    implements(INavigationTabs)

    def getNavigationMinisitePath(self):
        minisite = self.request.get('cpskin_minisite', None)
        if not isinstance(minisite, Minisite):
            portal = api.portal.get()
            return '/'.join(portal.getPhysicalPath())
        else:
            return minisite.search_path

    def _getNavQuery(self):
        query = super(MinisiteCatalogNavigationTabs, self)._getNavQuery()
        rootPath = self.getNavigationMinisitePath()
        query['path'] = {'query': rootPath, 'depth': 1}
        return query

    def topLevelTabs(self, actions=None, category='portal_tabs'):
        result = super(MinisiteCatalogNavigationTabs, self).topLevelTabs(
            None,
            'minisite'
        )
        item = api.content.get(self.getNavigationMinisitePath())

        home = {'name': _(u'home'),
                'id': item.getId,
                'url': item.absolute_url(),
                'description': item.Description}
        result.insert(0, home)
        return result


class MinisiteViewletMenu(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('minisite_menu.pt')

    def get_minisite_root(self):
        minisite = self.request.get('cpskin_minisite', None)
        obj = self.context
        portal = api.portal.get()
        while (not minisite.search_path == "/".join(obj.getPhysicalPath()) and
                aq_base(obj) is not aq_base(portal)):
            parent = aq_parent(aq_inner(obj))
            if parent is None:
                return obj
            obj = parent
        return obj

    def minisite_menu(self):
        minisite_root = self.get_minisite_root()
        if IHNavigationActivated.providedBy(minisite_root):
            return True
        else:
            return False
