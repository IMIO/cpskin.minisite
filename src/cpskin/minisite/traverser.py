from zope.interface import alsoProvides

from ZPublisher.BaseRequest import DefaultPublishTraverse

from cpskin.minisite.minisite import Minisite
from cpskin.minisite.interfaces import IInMinisite


class MinisiteTraverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        alsoProvides(request, IInMinisite)
        request.set('cpskin_minisite', Minisite())
        return super(MinisiteTraverser, self).publishTraverse(
            request, name)
