# Flashcard App

## Description

This is a simple flashcard application built with Python and the Tkinter library for the GUI interface. It enables users to create, review, and manage flashcards for efficient studying. The application employs the SuperMemo2 (SM2) algorithm for determining when flashcards should be reviewed based on user's self-assessed memory recall.

## Features

- Create and manage multiple flashcard decks.
- Add new flashcards to a deck.
- Review flashcards in a deck, with the option to view the back of the card.
- Grade your knowledge of a card from 0-5, which influences when the card will be reviewed next.
- Cards are stored and retrieved in/from a JSON file.

## Usage

1. Run the application by typing `python main.py` in your command line.
2. From the main menu, you can either create a new deck or browse existing decks.
3. When browsing decks, you can open a deck to review its flashcards.
4. When reviewing flashcards, you can click "Show Answer" to view the back of the card.
5. After viewing the answer, you can grade your knowledge of the card on a scale of 0-5.
6. You can also add new flashcards to the deck.

## Testing

Unit tests for the application are located in the `test.py` file. Run the tests by typing `python test.py` in your command line.


## Disclaimer

This is a learning project and should not be used for serious study purposes.
