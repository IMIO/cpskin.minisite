from plone import api


def get_minisite_object(request):
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return None
    return api.content.get(minisite.search_path)


def get_minisite_navigation_level(minisite_obj):
    portal = api.portal.get()
    portal_physical_path = portal.getPhysicalPath()
    minisite_physical_path = minisite_obj.getPhysicalPath()
    minisite_path = [elem for elem in list(minisite_physical_path) if elem not in list(portal_physical_path)]
    return len(minisite_path)
