import unittest
from unittest import mock
from main import Flashcard, FlashcardApp

class TestFlashcard(unittest.TestCase):
    def setUp(self):
        self.flashcard = Flashcard("front", "back")

    def test_to_dict(self):
        expected_dict = {
            'front': "front",
            'back': "back",
            'review_date': None,
            'interval': 1,
            'repetitions': 0,
            'easiness_factor': 2.5
        }
        self.assertEqual(self.flashcard.to_dict(), expected_dict)

    def test_from_dict(self):
        data = {
            'front': "front",
            'back': "back",
            'review_date': None,
            'interval': 1,
            'repetitions': 0,
            'easiness_factor': 2.5
        }
        flashcard = Flashcard.from_dict(data)
        self.assertEqual(flashcard.front, "front")
        self.assertEqual(flashcard.back, "back")
        self.assertEqual(flashcard.review_date, None)
        self.assertEqual(flashcard.interval, 1)
        self.assertEqual(flashcard.repetitions, 0)
        self.assertEqual(flashcard.easiness_factor, 2.5)


class TestFlashcardApp(unittest.TestCase):
    def setUp(self):
        self.app = FlashcardApp()

    def test_add_flashcard(self):
        self.app.add_flashcard("front", "back")
        self.assertEqual(len(self.app.flashcards), 1)
        self.assertEqual(self.app.flashcards[0].front, "front")
        self.assertEqual(self.app.flashcards[0].back, "back")

    # Since the 'load_flashcards' and 'save_flashcards' methods involve file IO, it's better to use 'mock' for testing them.
    # Here's a simple example of how to test 'load_flashcards' using 'unittest.mock'.
    @unittest.mock.patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"front": "front", "back": "back", "review_date": null, "interval": 1, "repetitions": 0, "easiness_factor": 2.5}]')
    def test_load_flashcards(self, mock_open):
        self.app.load_flashcards()
        self.assertEqual(len(self.app.flashcards), 1)
        self.assertEqual(self.app.flashcards[0].front, "front")
        self.assertEqual(self.app.flashcards[0].back, "back")


if __name__ == '__main__':
    unittest.main()