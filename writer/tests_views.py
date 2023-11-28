from probe.tests_django import DjangoTest


class DocumentViewTest(DjangoTest):
    def test_web_page(self):
        text = self.assertPageText(
            'http://shrinking-world.com', 210, 310, 'html')

    def test_pub_list_view(self):
        text = self.assertPageText('/writer/', 140, 210, 'html')

    def test_pub_view(self):
        text = self.assertPageText('/writer/ghost', 200, 290, 'html')

    def test_chapter_view(self):
        text = self.assertPageText(
            '/writer/ghost/WritersGuide', 240, 350, 'html')

    def test_doc_view(self):
        text = self.assertPageText(
            '/writer/ghost/WritersGuide/Chapter1.md', 310, 330, 'html')

    def test_ai_view(self):

        # Skip the Call to Open AI API
        # response = self.client.get('/ghost/Pub/Haiku.md/ai')
        # self.assertEqual(response.status_code, 302)

        self.assertPageText('/writer/ghost/Pub/Haiku.md', 140, 300, 'Haiku')


# class DocumentModelTest(DjangoTest):
#     def setUp(self):
#         self.document = Document.objects.create(
#             pub='Publication',
#             chapter='Chapter 1'
#         )

#     def test_document_str_representation(self):
#         self.assertEqual(str(self.document), 'Publication - Chapter 1')
