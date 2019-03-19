# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from cpskin.minisite.utils import get_acquired_base_object
from cpskin.minisite.utils import get_minisite_object
from cpskin.minisite.utils import url_in_portal_mode
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.transformchain.interfaces import ITransform
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface import Interface


def change_a_href(soup, request, html_id='content'):
    """
    """
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return
    minisite_obj = get_minisite_object(request)
    id_tag = soup.find(id=html_id)
    if id_tag:
        a_tags = id_tag.find_all('a')
        for tag in a_tags:
            href = tag.get('href')
            if not href:
                continue
            end_of_url = href.replace(minisite.minisite_url, '')
            container = get_acquired_base_object(minisite_obj, end_of_url)
            if container is None:
                continue
            container_url = url_in_portal_mode(container, request)
            container_url = container_url.rstrip('/')
            tag['href'] = '{0}{1}'.format(container_url, end_of_url)


class Minisite(object):
    implements(ITransform)
    adapts(Interface, Interface)
    order = 9000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def applyTransform(self):
        # if not in minisite False
        site = getSite()
        if not site:
            return False

        responseType = self.request.response.getHeader('content-type') or ''
        if not responseType.startswith('text/html') and \
                not responseType.startswith('text/xhtml'):
            return False
        return True

    def transformBytes(self, result, encoding):
        if not self.applyTransform():
            return result
        soup = BeautifulSoup(result, 'lxml')
        change_a_href(soup, self.request)
        return str(soup)

    def transformUnicode(self, result, encoding):
        if not self.applyTransform():
            return result
        soup = BeautifulSoup(result, 'lxml')
        change_a_href(soup, self.request)
        return str(soup)

    def transformIterable(self, result, encoding):
        if not self.applyTransform():
            return result
        transformed = []
        for r in result:
            soup = BeautifulSoup(r, 'lxml')
            change_a_href(soup, self.request)
            transformed.append(str(soup))

        return transformed
