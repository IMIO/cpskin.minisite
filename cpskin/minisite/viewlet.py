from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxBase


class MinisiteViewlet(ViewletBase):

    pass


class SearchBoxViewlet(SearchBoxBase):
    index = ViewPageTemplateFile('searchbox.pt')
