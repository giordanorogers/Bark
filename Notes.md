# To add a new feature to Bark:

## Data Persistence
Add in the database module

## Business Logic
Add in the commands module

## User Interaction
Add in the bark module

### TIP:
Duplicating some code and updating that new copy to do what you need is a perfectly valid
approach to extension.
By creating a duplicate version, altering it, and seeing how the two versions differ,
we can more easily refactor that duplicated code back into a single, multipurpose
version later.

```
choices = {
    'A': 'apples',
    'B': 'bananas'
}

for choice in choices.keys():
    print(f'{choice} is for {choices[choice]}')

```

The loose coupling we've used writing Bark means that new database functionality
can be added with new methods on the DatabaseManager class or with focused
changes to an existing (centralized) method. New business logic can be encapsulated
in the new Command classes, and adding to the menu is a matter of creating a new option
in the options dictionary in the bark module and hooking it up to a command.