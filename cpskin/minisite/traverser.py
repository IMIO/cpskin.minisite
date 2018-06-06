# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import IContentish
from collective.redirectacquired.traverse import LogAcquiredImageTraverser
from collective.redirectacquired.traverse import LogAcquiredPublishTraverse
from cpskin.minisite import logger
from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.minisite import decorateRequest
from cpskin.minisite.portlet import checkPortlet
from plone.rest.interfaces import IAPIRequest
from plone.rest.traverse import RESTTraverse
from zope.component import queryUtility


class MinisiteTraverser(LogAcquiredPublishTraverse):

    def publishTraverse(self, request, name):
        if IAPIRequest.providedBy(request):
            rest_traverser = RESTTraverse(self.context, self.request)
            result = rest_traverser.publishTraverse(request, name)
        else:
            result = super(MinisiteTraverser, self).publishTraverse(
                request, name)
        if IContentish.providedBy(result):
            path = '/'.join(result.getPhysicalPath())
            logger.debug('Traversing {0}'.format(path))
            config = queryUtility(IMinisiteConfig, name=path)
            decorateRequest(request, config)
            checkPortlet(request, config)
        return result


class MinisiteImageTraverser(LogAcquiredImageTraverser):

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
