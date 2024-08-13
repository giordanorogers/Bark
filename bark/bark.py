import os
import requests
from commands import commands
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):

        # Store the prep call information (optional)
        data = self.prep_call() if self.prep_call else None

        if data:
            # Execute the prep call (optional)
            message = self.command.execute(data)
        else:
            # Execute the Option's command (default)
            message = self.command.execute()

        # Print the message returned from sql execution.
        print(message)

    def __str__(self):
        # Return the Option's name as the class string
        return self.name


def print_options(options: dict) -> None:
    """Prints the keys(shortcuts) and values(option details) for an input options dictionary."""
    for shortcut, option in options.items():
        print(f"({shortcut})  {option}")
    print()


def option_choice_is_valid(choice, options: dict):
    """Returns the keys from the input options dictionary."""
    return choice in options or choice.upper() in options


def get_option_choice(options: dict):

    # Store the user's option shortcut input
    choice = input('Choose an option: ')

    # Loop while input is invalid
    while not option_choice_is_valid(choice, options):
        print('Invalid input')
        choice = input('Choose an option: ')

    # Return the Option object associated with the user input.
    return options[choice.upper()]


# A general function for prompting user for input
def get_user_input(label, required=True):

    # Catch user input
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


def get_github_data():

    username = get_user_input('Username: ')
    preserve_timestamps = get_user_input('Preserve timestamps? [Y/n] :')
    if username == "giordanorogers":
        token = os.environ['GITHUB_TOKEN']
    else:
        token = None

    if preserve_timestamps == 'Y' or preserve_timestamps == 'y':
        timestamp_bool = True
    else:
        timestamp_bool = False

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Send the GET request
    response = requests.get('https://api.github.com/user/starred', headers=headers)

    stars_data = []
    for star in response.json():
        star_bookmark = {
            'title': star['name'],
            'url': star['html_url'],
            'date_added': star['created_at']
        }
        stars_data.append(star_bookmark)

    return stars_data, timestamp_bool

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
        'G': Option('Import GitHub stars', commands.ImportGitHubStarsCommand(), prep_call=get_github_data),
        'Q': Option('Quit', commands.QuitCommand())
    }

    print_options(options)

    chosen_option = get_option_choice(options)

    clear_screen()

    chosen_option.choose()

    _ = input('Press Enter to return to main menu')


if __name__ == '__main__':

    # Create the bookmarks table if it doesn't already exist.
    commands.CreateBookmarksTableCommand().execute()

    # Loop the menu until the user quits.
    while True:
        loop()