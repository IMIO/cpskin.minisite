from zope.component import provideUtility

from cpskin.minisite.minisite import Minisite


def registerMinisites(event):
    minisite = Minisite()
    provideUtility(
        minisite,
        name=u"/plone/minisite",
    )


def registerMinisitesSetupHandler(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile(
            'register_cpskin_minisites.txt') is None:
        return
    registerMinisites(None)
