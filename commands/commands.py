import sys
from datetime import datetime
from database.database import DatabaseManager

db = DatabaseManager('./database/bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand:
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark Added'


class ImportGitHubStarsCommand:
    def execute(self, stars_data_and_timestamp):

        stars_data, timestamp = stars_data_and_timestamp

        for star in stars_data:
            if timestamp:
                db.add('bookmarks', star)
            else:
                star['date_added'] = datetime.utcnow().isoformat()
                db.add('bookmarks', star)
        return 'Stars Imported'


class ListBookmarksCommand:
    # Accept the column to order by, and save it as an instance attribute
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    # Pass this info along to db.select
    def execute(self):
        query = db.select('bookmarks', order_by=self.order_by)
        return query.fetchall()


class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return f'Bookmark {data} deleted'


class QuitCommand:
    def execute(self):
        sys.exit()
