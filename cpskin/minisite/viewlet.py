from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase
from plone.app.portlets.portlets.navigation import getRootPath
from plone import api
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


# class MinisiteQueryBuilder(QueryBuilder):
#     implements(INavigationQueryBuilder)
#     adapts(Interface, INavigationPortlet)
#
#     def __call__(self):
#         topLevel = calculateTopLevel(self.context, self.portlet)
#         self.query['path']['navtree_start'] = topLevel + 1
#         return self.query
#
#
# class MinisiteNavtreeStrategy(NavtreeStrategy):
#     implements(INavtreeStrategy)
#     adapts(Interface, INavigationPortlet)
#
#     def __init__(self, context, portlet):
#         NavtreeStrategy.__init__(self, context, portlet)
#         portal_properties = getToolByName(context, 'portal_properties')
#         navtree_properties = getattr(portal_properties, 'navtree_properties')
#         currentFolderOnly = portlet.currentFolderOnly or \
#             navtree_properties.getProperty('currentFolderOnlyInNavtree', False)
#         topLevel = calculateTopLevel(context, portlet)
#         self.rootPath = getRootPath(context, currentFolderOnly, topLevel, portlet.root)


class MinisiteViewletMenu(ViewletBase):
    index = ViewPageTemplateFile('minisite_menu.pt')

    def get_tabs(self):
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                       name='portal_tabs_view')


    def getNavRootPath(self):
        currentFolderOnly = True

        topLevel = calculate_top_level(self.context)
        root = '/'.join(
            api.portal.get_navigation_root(self.context).getPhysicalPath())

        if isinstance(root, unicode):
            root = str(root)
        root_path = getRootPath(self.context, currentFolderOnly, topLevel, root)
        return api.content.get(root_path)

    def selectedClass(self):
        # if selected...
        return 'selected'
