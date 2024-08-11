import os
from collections import OrderedDict
from commands import commands


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None

        if data:
            message = self.command.execute(data)
        else:
            message = self.command.execute()

        print(message)

    def __str__(self):
        return self.name


def print_options(options):
    for shortcut, option in options.items():
        print(f"({shortcut})  {option}")
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid input')
        choice = input('Choose an option: ')
    return options[choice.upper()]


# A general function for prompting user for input
def get_user_input(label, required=True):
    value = input(f'{label}: ') or None

    # Keep prompting while input is empty, if required
    while required and not value:
        value = input(f'{label}: ') or None
    return value


# Function to get the necessary data for adding a new bookmark
def get_new_bookmark_data():
    bookmark = {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),
    }
    return bookmark


# Gets the necessary information for deleting a bookmark
def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

def loop():
    clear_screen()

    print('BARK Commands:\n',
          '--------------')

    options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
        'Q': Option('Quit', commands.QuitCommand())
    }

    print_options(options)

    chosen_option = get_option_choice(options)

    clear_screen()

    chosen_option.choose()

    _ = input('Press Enter to return to main menu')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()