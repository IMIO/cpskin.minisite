from zope.interface import alsoProvides
from zope.component import queryUtility

from ZPublisher.BaseRequest import DefaultPublishTraverse

from cpskin.minisite.interfaces import IMinisite
from cpskin.minisite.interfaces import IInMinisite


class MinisiteTraverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        path = "/".join(self.context.getPhysicalPath() + (name,))
        minisite = queryUtility(IMinisite, name=path)
        if minisite:
            alsoProvides(request, IInMinisite)
            request.set('cpskin_minisite', minisite)
        return super(MinisiteTraverser, self).publishTraverse(
            request, name)
