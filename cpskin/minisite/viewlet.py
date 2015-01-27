from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase


class MinisiteViewlet(ViewletBase):
    index = ViewPageTemplateFile('minisite_in_minisite.pt')

    def url_in_portal_mode(self):
        portal_url = getToolByName(self.context, 'portal_url')
        relative_url = portal_url.getRelativeContentURL(self.context)
        portal = portal_url.getPortalObject()
        main_portal_url = self.request.cpskin_minisite.main_portal_url
        minisite_urls = self.request.cpskin_minisite.minisite_urls
        root_url = portal.absolute_url()
        for minisite_url in minisite_urls:
            if root_url.startswith(minisite_url):
                root_url_in_portal_mode = root_url.replace(
                    minisite_url,
                    main_portal_url
                )
        return '/'.join((root_url_in_portal_mode, relative_url))


class SearchBoxViewlet(SearchBoxBase):
    index = ViewPageTemplateFile('searchbox_in_minisite.pt')
