from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.controlpanel.security import ISecuritySchema

from plone.testing import z2
from plone import api

import cpskin.minisite


class CPSkinMinisiteLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        super(CPSkinMinisiteLayer, self).setUpPloneSite(portal)
        ISecuritySchema(portal).set_enable_self_reg(True)


CPSKIN_MINISITE = CPSkinMinisiteLayer(
    name='CPSKIN_MINISITE',
    zcml_package=cpskin.minisite,
    zcml_filename='testing.zcml',
    gs_profile_id='cpskin.minisite:testing',
)

CPSKIN_MINISITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_MINISITE,),
    name="CPSKIN_MINISITE_INTEGRATION_TESTING"
)
CPSKIN_MINISITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_MINISITE, z2.ZSERVER_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE),
    name="CPSKIN_MINISITE_FUNCTIONAL_TESTING"
)
