# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from cpskin.minisite.utils import get_acquired_base_object
from cpskin.minisite.utils import get_minisite_object
from cpskin.minisite.utils import url_in_portal_mode
from plone.transformchain.interfaces import ITransform
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.interface import implements

IDS_WITH_HREF = [
    'content-core',
    'viewlet-below-content-body',
]

CLASSES_WITH_HREF = [
    'parsable-content',
]


def change_a_href(soup, request, html_ids=[], html_classes=[]):
    """
    """
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return
    minisite_obj = get_minisite_object(request)
    tags = [soup.find(id=html_id) for html_id in html_ids]
    for cl in html_classes:
        tags.extend(soup.find_all(class_=cl))
    for tag in tags:
        if tag is None:
            continue
        a_tags = tag.find_all('a')
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
            tag['target'] = '_blank'


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
        change_a_href(soup, self.request, IDS_WITH_HREF, CLASSES_WITH_HREF)
        return str(soup)

    def transformUnicode(self, result, encoding):
        if not self.applyTransform():
            return result
        soup = BeautifulSoup(result, 'lxml')
        change_a_href(soup, self.request, IDS_WITH_HREF, CLASSES_WITH_HREF)
        return str(soup)

    def transformIterable(self, result, encoding):
        if not self.applyTransform():
            return result
        transformed = []
        for r in result:
            soup = BeautifulSoup(r, 'lxml')
            change_a_href(soup, self.request, IDS_WITH_HREF, CLASSES_WITH_HREF)
            transformed.append(str(soup))

        return transformed
