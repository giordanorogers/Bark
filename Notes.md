Each action is kind of like a command that needs to be executed in response to a user's menu choice.
By encapsulating the logic of each action as a command object, 
and providing a consistent way to trigger them via an execute methods, 
these actions can be decoupled from the presentation layer. 
The presentation layer can then point menu options to commands without worrying about how those commands work.
This is called the command pattern.

Based on what you've learned about encapsulation, 
how would you go about hooking up the items in the presentation layer to the
business logic they control?
Make a class that pairs the text to be displayed to the user and the command it triggers.

With the Option class in place, now is a good time to start hooking up more of the 
business logic you created earlier.
Remember that you need to do a few things with each option:
1. Print the keyboard key for the user to enter to choose the option.
2. Print the option text.
3. Check if the user's input matches an option and, if so, choose it.

Each keyboard key maps to a menu option, and you need to check the user's input
against the available options, so you need to keep those pairings stored somehow.
A dictionary is good because a dict can provide keyboard key and option pairs that
you can also iterate over, with the dicitonary's .items() method, for printing
the option text.
I also recommed using collections.OrderedDict specifically, to ensure
that your menu options will always be printed in the order you specify.

The approach for getting the user's desired option goes like this:
1. Prompt the user to enter a choice, using Python's built-in input function.
2. If the user's choice matches one of those listed, call that option's choose method.
3. Otherwise, repeat

You need to supply a title, description, and so on to add a bookmark,
and you need to specify the ID of a bookmark to delete it.
Much like you got user input for the menu option to choose,
you'll need to prompt the user for this bookmark data.
Here's another opportunity to encapsulate some behavior.
For each piece of information you need, you should
1. Prompt the user with a label--"Title" or "Description", for example
2. If the information is required and the user presses Enter without entering any info, keep prompting them

Write three functions--one to provide the repeating prompt behavior, and two that use
it to get information for adding or deleting a bookmark.
Then add each information-fetching function as the prep_call to the appropriate Option instance.