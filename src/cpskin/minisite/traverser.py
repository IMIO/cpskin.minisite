from zope.component import queryUtility

from ZPublisher.BaseRequest import DefaultPublishTraverse

from plone.app.imaging.traverse import ImageTraverser

from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.minisite import decorateRequest


class MinisiteTraverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        path = "/".join(self.context.getPhysicalPath())
        config = queryUtility(IMinisiteConfig, name=path)
        decorateRequest(request, config)
        return super(MinisiteTraverser, self).publishTraverse(
            request, name)


class MinisiteImageTraverser(ImageTraverser):

    def publishTraverse(self, request, name):
        path = "/".join(self.context.getPhysicalPath())
        config = queryUtility(IMinisiteConfig, name=path)
        decorateRequest(request, config)
        return super(MinisiteImageTraverser, self).publishTraverse(
            request, name)
