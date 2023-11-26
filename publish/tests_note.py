
from django.test import TestCase

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
        self.assertEquals(f'{note.title}', 'first note')
        self.assertEquals(f'{note.text}', 'a note')
        self.assertEquals(f'{note.author}', 'Abe Lincoln')
        self.assertEquals(f'{note.published}', 'True')

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

    def test_note_list_view(self):
        # no notes
        response = self.client.get('/note/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no notes to edit.')

        # with notes
        create_note(title='first note')
        create_note(title='second note')
        response = self.client.get('/note/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<li>', 2)
        self.assertContains(response, 'first note')
        self.assertContains(response, 'Mark Seaman')
