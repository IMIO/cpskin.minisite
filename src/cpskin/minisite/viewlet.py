from plone.app.layout.viewlets.common import ViewletBase


class MinisiteViewlet(ViewletBase):

    def is_in_portal_mode(self):
        request = self.request
        main_portal_url = request.cpskin_minisite.main_portal_url
        return request.URL.startswith(main_portal_url)

    def is_in_minisite_mode(self):
        request = self.request
        minisite_url = request.cpskin_minisite.minisite_url
        return request.URL.startswith(minisite_url)
