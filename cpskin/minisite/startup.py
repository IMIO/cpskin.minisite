import ConfigParser
import os.path

from zope.component import provideUtility

from cpskin.minisite.minisite import MinisiteConfig
from cpskin.minisite import logger


def registerMinisites(event):
    CLIENT_HOME = os.environ["CLIENT_HOME"]
    minisites_directory = os.path.join(CLIENT_HOME, 'minisites')
    if os.path.exists(minisites_directory):
        registerMinisitesFromDirectory(minisites_directory)


def registerMinisitesFromDirectory(directory):
    files = os.listdir(directory)
    for filename in files:
        filename = os.path.join(directory, filename)
        if os.path.isfile(filename):
            registerMinisitesFromFile(filename)


def registerMinisitesFromFile(filename):
    config = ConfigParser.RawConfigParser()
    try:
        config.read(filename)
    except ConfigParser.MissingSectionHeaderError:
        return
    logger.debug('Register minisites from file {}'.format(filename))
    # import ipdb;ipdb.set_trace()
    for section in config.sections():
        try:
            portal_url = config.get(section, 'portal_url')
            # XXX check if path is unique
            try:
                minisite_urls = config.get(section, 'minisite_urls')
            except:
                minisite_urls = config.get(section, 'minisite_url')
            minisite_url_list = [minisite_url.strip() for minisite_url in minisite_urls.split(',')]
            minisite = MinisiteConfig(
                main_portal_url=portal_url,
                minisite_urls=minisite_url_list,
                search_path=section,
                filename=filename,
            )
            registerMinisite(minisite)
        except KeyError:
            continue


def registerMinisite(config):
    logger.debug('Register minisite at {} for {}'.format(
        config.main_portal_url,
        ", ".join(config.minisite_urls),
        )
    )
    provideUtility(
        config,
        name=config.search_path,
    )


def registerMinisitesSetupHandler(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile(
            'register_cpskin_minisites.txt') is None:
        return
    from cpskin.minisite import tests

    filename = os.path.join(
        os.path.dirname(tests.__file__),
        'minisites_config.txt',
    )

    registerMinisitesFromFile(filename)
