from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

from plone.testing import z2

import cpskin.minisite

CPSKIN_MINISITE = PloneWithPackageLayer(
    name='CPSKIN_MINISITE',
    zcml_package=cpskin.minisite,
    zcml_filename='configure.zcml',
    gs_profile_id='cpskin.minisite:default',
)

CPSKIN_MINISITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_MINISITE,),
    name="CPSKIN_MINISITE_INTEGRATION_TESTING"
)
CPSKIN_MINISITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_MINISITE, z2.ZSERVER_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE),
    name="CPSKIN_MINISITE_FUNCTIONAL_TESTING"
)
