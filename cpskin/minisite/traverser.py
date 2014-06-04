from zope.component import queryUtility

from ZPublisher.BaseRequest import DefaultPublishTraverse

from plone.app.imaging.traverse import ImageTraverser
from Products.CMFCore.interfaces import IContentish

from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.minisite import decorateRequest
from cpskin.minisite import logger


class MinisiteTraverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        result = super(MinisiteTraverser, self).publishTraverse(
            request, name)
        if IContentish.providedBy(result):
            path = "/".join(result.getPhysicalPath())
            logger.info('Traversing {}'.format(path))
            config = queryUtility(IMinisiteConfig, name=path)
            decorateRequest(request, config)
        return result


class MinisiteImageTraverser(ImageTraverser):

    def publishTraverse(self, request, name):
        result = super(MinisiteImageTraverser, self).publishTraverse(
            request, name)
        if IContentish.providedBy(result):
            path = "/".join(result.getPhysicalPath())
            logger.info('Traversing {}'.format(path))
            config = queryUtility(IMinisiteConfig, name=path)
            decorateRequest(request, config)
        return result
