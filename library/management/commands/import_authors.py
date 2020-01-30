import csv
from django.core.management.base import BaseCommand, CommandError
from library.models import Author


class Command(BaseCommand):
    help = "Imports a .csv file containing authors' names and inserts them into database."

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='File name (with extension).')

    def handle(self, *args, **options):
        filename = options['file']
        if not filename:
            raise CommandError('No file was specified.')
        has_errors = False
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            try:
                authors = [Author(name=row['name']) for row in reader]
            except KeyError:
                # File is not in the correct format, with 1st column being "name".
                has_errors = True
        if has_errors:
            self.stdout.write(self.style.ERROR('File is in incorrect format. It must have a "name" column.'))
            return
        created_authors = Author.objects.bulk_create(authors, ignore_conflicts=True)
        created_authors_count = len(created_authors)
        if not created_authors_count:
            self.stdout.write(self.style.WARNING('File was imported successfully but could not register any author.'))
            return
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported author file and registered {created_authors_count} '
                f'author{"s" if created_authors_count != 1 else ""}. '
            )
        )
