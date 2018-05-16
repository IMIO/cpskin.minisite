# -*- coding: utf-8 -*-
from cpskin.minisite import logger
from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.minisite import decorateRequest
from cpskin.minisite.portlet import checkPortlet
from plone.app.imaging.traverse import ImageTraverser
from plone.rest.interfaces import IAPIRequest
from plone.rest.traverse import RESTTraverse
from Products.CMFCore.interfaces import IContentish
from zope.component import queryUtility
from ZPublisher.BaseRequest import DefaultPublishTraverse


class MinisiteTraverser(RESTTraverse):

    def publishTraverse(self, request, name):
        if IAPIRequest.providedBy(request):
            result = RESTTraverse.publishTraverse(self, request, name)
        else:
            result = DefaultPublishTraverse.publishTraverse(
                self,
                request,
                name
            )
        if IContentish.providedBy(result):
            path = '/'.join(result.getPhysicalPath())
            logger.debug('Traversing {0}'.format(path))
            config = queryUtility(IMinisiteConfig, name=path)
            decorateRequest(request, config)
            checkPortlet(request, config)
        return result


class MinisiteImageTraverser(ImageTraverser):

    def publishTraverse(self, request, name):
        result = super(MinisiteImageTraverser, self).publishTraverse(
            request, name)
        if IContentish.providedBy(result):
            path = '/'.join(result.getPhysicalPath())
            logger.debug('Traversing {0}'.format(path))
            config = queryUtility(IMinisiteConfig, name=path)
            decorateRequest(request, config)
            checkPortlet(request, config)
        return result
