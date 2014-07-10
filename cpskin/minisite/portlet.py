from Acquisition import aq_inner
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cpskin.minisite.interfaces import IInMinisite
from cpskin.minisite.viewlet import MinisiteViewlet


class IMiniSitePortlet(IPortletDataProvider):
    """
    Mini Site portlet interface
    """


class Assignment(base.Assignment):
    implements(IMiniSitePortlet)

    @property
    def title(self):
        return "Mini site"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')

    @property
    def available(self):
        request = self.request
        return IInMinisite.providedBy(request)

    def viewlet(self):
        context = self.context
        request = self.request
        context = aq_inner(context)
        viewlet = MinisiteViewlet(context, request, None, None).__of__(context)
        viewlet.update()
        return viewlet.render()


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
