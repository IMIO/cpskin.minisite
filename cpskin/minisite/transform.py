# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.transformchain.interfaces import ITransform
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface import Interface


def change_a_href(soup, request, html_id='content-core'):
    """
    """
    id_tag = soup.find(id=html_id)
    if id_tag:
        a_tags = id_tag.find_all('a')
        for tag in a_tags:
            href = tag.get('href')
            minisite = request.get('cpskin_minisite', None)
            end_of_url = href.replace(minisite.minisite_url, '')
            portal_href_url = '{0}{1}'.format(minisite.search_path, end_of_url)
            href_obj = api.content.get(portal_href_url)
            if href_obj and IDexterityContent.providedBy(href_obj):
                if not '/'.join(href_obj.getPhysicalPath()).startswith(
                        minisite.search_path):
                    tag['href'] = href.replace(
                        minisite.minisite_url,
                        minisite.main_portal_url
                    )


class Minisite(object):
    implements(ITransform)
    adapts(Interface, Interface)
    order = 9000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def applyTransform(self):
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
        change_a_href(soup, self.request, 'viewlet-below-content-body')
        return str(soup)

    def transformUnicode(self, result, encoding):
        if not self.applyTransform():
            return result
        soup = BeautifulSoup(result, 'lxml')
        change_a_href(soup, self.request)
        change_a_href(soup, self.request, 'viewlet-below-content-body')
        return str(soup)

    def transformIterable(self, result, encoding):
        if not self.applyTransform():
            return result
        transformed = []
        for r in result:
            soup = BeautifulSoup(r, 'lxml')
            change_a_href(soup, self.request)
            change_a_href(soup, self.request, 'viewlet-below-content-body')
            transformed.append(str(soup))

        return transformed
