from django.test import TestCase


class ViewTest(TestCase):

    def test_html_page_view(self):
        response = self.client.get('/views/')
        # self.assertContains(response, 'App Workshop')

    #     response = self.client.get('/views/workshop.html')
    #     self.assertContains(response, 'Home Page')

    #     response = self.client.get('/views/theme.html')
    #     self.assertContains(response, 'No Page Content')

    #     response = self.client.get('/views/page.html')
    #     self.assertContains(response, 'Generic HTML Page')

    # def test_card_view(self):
    #     response = self.client.get('/views/card')
    #     self.assertContains(response, 'Card Four')

    # def test_document_view(self):
    #     response = self.client.get('/views/doc/')
    #     self.assertContains(response, 'Doc Index')

    # def test_tabs_view(self):
    #     response = self.client.get('/views/tabs')
    #     self.assertContains(response, 'Card Four')

    # def test_accordion_view(self):
    #     response = self.client.get('/views/accordion')
    #     self.assertContains(response, 'Week 12')

    # def test_carousel_view(self):
    #     response = self.client.get('/views/carousel')
    #     self.assertContains(response, 'Ocean')
