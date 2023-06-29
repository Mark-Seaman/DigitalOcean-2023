from probe.tests_django import DjangoTest


class DocumentViewTest(DjangoTest):
    def test_web_page(self):
        text = self.assertPageText( 'http://shrinking-world.com', 210, 300, 'html')

    def test_pub_list_view(self):
        text = self.assertPageText('/writer/', 180, 210, 'html')

    def test_pub_view(self):
        text = self.assertPageText('/writer/GhostWriter', 240, 280, 'html')

    def test_chapter_view(self):
        text = self.assertPageText('/writer/GhostWriter/WritersGuide', 240, 340, 'html')

    def test_doc_view(self):
        text = self.assertPageText(
            '/writer/GhostWriter/WritersGuide/Chapter1.md', 290, 310, 'html')

    def test_ai_view(self):

        # Skip the Call to Open AI API
        # response = self.client.get('/GhostWriter/Pub/Haiku.md/ai')
        # self.assertEqual(response.status_code, 302)

        self.assertPageText('/writer/GhostWriter/Pub/Haiku.md', 140, 300, 'Haiku')


# class DocumentModelTest(DjangoTest):
#     def setUp(self):
#         self.document = Document.objects.create(
#             pub='Publication',
#             chapter='Chapter 1'
#         )

#     def test_document_str_representation(self):
#         self.assertEqual(str(self.document), 'Publication - Chapter 1')
