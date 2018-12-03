# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.redirectacquired.traverse import LogAcquiredImageTraverser
from collective.redirectacquired.traverse import LogAcquiredPublishTraverse
from cpskin.minisite import logger
from cpskin.minisite.interfaces import IMinisiteConfig
from cpskin.minisite.minisite import decorateRequest
from cpskin.minisite.portlet import checkPortlet
from cpskin.minisite.utils import get_minisite_object
from cpskin.minisite.utils import url_in_portal_mode
from OFS.interfaces import IItem
from plone import api
from plone.rest.interfaces import IAPIRequest
from plone.rest.traverse import RESTTraverse
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from zExceptions import Redirect
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from ZPublisher.interfaces import IPubAfterTraversal


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


def get_acquired_base_object(minisite, name):
    obj = minisite
    while (not IPloneSiteRoot.providedBy(obj) and
           not safe_hasattr(aq_base(obj), name)):
        parent = aq_parent(aq_inner(obj))
        if parent is None:
            break
        obj = parent
    return obj


@adapter(IPubAfterTraversal)
def redirect(event):
    white_list_name = [
        'portal_javascripts',
        'portal_css',
    ]
    white_list_end = (
        '.png',
        '.gif',
        '.ico',
        # '.jpeg',
        # '.jpg',
    )
    request = event.request
    parents = request['PARENTS']

    minisite = get_minisite_object(request)
    if not minisite:
        return

    minisite_index = parents.index(minisite)
    first_child = parents[minisite_index - 1]
    if not safe_hasattr(first_child, 'getId'):
        return

    first_name = first_child.getId()
    if not first_name:
        return

    if first_name in white_list_name \
            or first_name.startswith('++') \
            or first_name.endswith(white_list_end):
        logger.debug('Found a white list {0}'.format(first_name))
        return

    if safe_hasattr(aq_base(minisite), first_name):
        # no acquisition used here, object is in minisite
        logger.debug('No acquisition detected to {0}'.format(first_name))
        return

    obj = queryMultiAdapter((minisite, request), name=first_name)
    if obj and not IItem.providedBy(obj):
        # it's a view
        logger.debug('Found a view for {0}'.format(first_name))
        return

    base_object = get_acquired_base_object(minisite, first_name)
    redirect_base_url = url_in_portal_mode(base_object, request)
    redirect_base_url = redirect_base_url.rstrip('/')

    portal_url = api.portal.get().absolute_url()
    portal_url = portal_url.rstrip('/')
    redirect_url = request['URL'].replace(portal_url, redirect_base_url)

    logger.info('Redirecting to {0} {1}'.format(redirect_url, first_name))
    if redirect_url.endswith('/index_html'):
        redirect_url = redirect_url.replace('/index_html', '')
    raise Redirect(redirect_url)
