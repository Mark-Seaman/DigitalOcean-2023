from django.test import TestCase
from django.contrib.auth.models import User
from publish.note import create_note, get_note_id, notes, set_note
from .models import Note


class NoteDataTest(TestCase):

    def test_default_note(self):
        note = create_note()
        self.assertEquals(note.title, 'No title')
        self.assertEquals(note.text, 'None')
        self.assertEquals(note.author, 'Mark Seaman')
        self.assertEquals(note.published, False)

    def test_text_content(self):
        create_note(title='first note', text='a note',
                    author='Abe Lincoln', published=True)
        note = get_note_id(1)
        self.assertEqual(note.title, 'first note')
        self.assertEqual(note.text, 'a note')
        self.assertEqual(note.author, 'Abe Lincoln')
        self.assertEqual(note.published, True)

    def test_note_list(self):
        create_note()
        self.assertEqual(len(notes(title='No title')), 1)
        self.assertEqual(len(notes(author='Me')), 0)

    def test_set_note(self):
        create_note()
        note = set_note(title='No title', text='My text', published=True)
        self.assertEquals(note.title, 'No title')
        self.assertEquals(note.text, 'My text')
        self.assertEquals(note.author, 'Mark Seaman')
        self.assertEquals(note.published, True)


class NoteViewTest(TestCase):
    def setUp(self):
        # create a user for login
        self.user = User.objects.create_user(
            username='johndoe',
            password='password')

    def test_note_list_view(self):
        # no notes
        response = self.client.get('/note/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no notes to edit.')

        # with notes
        create_note(title='first note', published=True)
        create_note(title='second note', published=True)
        response = self.client.get('/note/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<tr>', 3)
        self.assertContains(response, 'first note')
        self.assertContains(response, 'Mark Seaman')
        self.assertTemplateUsed(response, 'note/note_list.html')

    def test_note_detail_view(self):
        create_note()
        response = self.client.get('/note/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No title')
        self.assertContains(response, 'Mark Seaman')
        self.assertTemplateUsed(response, 'note/note_detail.html')

    def test_note_create_view(self):
        response = self.client.get('/note/add')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No title')
        self.assertTemplateUsed(response, 'note/note_form.html')

        # create a note
        response = self.client.post('/note/add', {'title': 'first note'})
        self.assertEqual(response.status_code, 302)
        note = get_note_id(1)
        self.assertEquals(f'{note.title}', 'first note')

    def test_note_update_view(self):
        # update note without login
        create_note()
        data = dict(title='Updated note', text='OK',
                    author='Me', published=True)
        response = self.client.post('/note/1/', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/note/1/')

        # update note with login
        self.assertTrue(self.client.login(
            username='johndoe', password='password'))
        response = self.client.post('/note/1/', data)
        self.assertEqual(response.status_code, 302)

        # test values
        note = get_note_id(1)
        self.assertEqual(note.title, 'Updated note')
        self.assertEquals(note.text, 'OK')
        self.assertEquals(note.author, 'Me')
        self.assertEquals(note.published, True)

    def test_note_delete_view(self):
        # delete note confirmation
        create_note()
        response = self.client.get('/note/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure ")
        self.assertTemplateUsed(response, 'note/note_delete.html')

        # delete note
        response = self.client.post('/note/1/delete')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(notes()), 0)
        self.assertRedirects(response, '/note/')
