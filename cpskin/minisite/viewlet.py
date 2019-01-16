from zope.interface import implements
from zope.component import getUtilitiesFor

from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.interfaces import INavigationTabs
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase
from plone import api

from cpskin.minisite.browser.interfaces import IHNavigationActivated
from cpskin.minisite.utils import get_minisite_object
from cpskin.minisite.utils import url_in_portal_mode
from cpskin.minisite.minisite import Minisite
from cpskin.minisite.interfaces import IMinisiteConfig


class MinisiteViewlet(ViewletBase):
    index = ViewPageTemplateFile('minisite_in_minisite.pt')

    def url_in_portal_mode(self):
        return url_in_portal_mode(self.context, self.request)


class SearchBoxViewlet(SearchBoxBase):
    index = ViewPageTemplateFile('searchbox_in_minisite.pt')


class MinisiteCatalogNavigationTabs(CatalogNavigationTabs):
    implements(INavigationTabs)

    def getNavigationMinisitePaths(self):
        portal_path = '/'.join(self.context.getPhysicalPath())
        configs = getUtilitiesFor(IMinisiteConfig, self.context)
        result = [
            config.search_path for name, config in configs
            if config.search_path.startswith(portal_path)
        ]

        return result

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
            actions,
            'minisite'
        )
        item = api.content.get(self.getNavigationMinisitePath())

        home = {'name': '',
                'id': item.getId(),
                'url': item.absolute_url(),
                'description': item.Description,
                'class': 'minisite-home'}
        result.insert(0, home)
        return result


class MinisiteViewletMenu(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('minisite_menu.pt')

    def update(self):
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='ms_portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)

        self.selected_portal_tab = self.selected_tabs['portal']
        self.minisite_root = get_minisite_object(self.request)

    def minisite_menu(self):
        if IHNavigationActivated.providedBy(self.minisite_root):
            return True
        else:
            return False

    def actions(self):
        minisite = self.request.get('cpskin_minisite', None)
        if not isinstance(minisite, Minisite):
            return []
        portal = api.portal.get()
        minisiteRoot = portal.unrestrictedTraverse(minisite.search_path)
        actions = api.content.find(
            context=minisiteRoot,
            hiddenTags='minisite-action',
            sort_on='getObjPositionInParent',
        )
        return actions
