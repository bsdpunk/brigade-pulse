from django.core.management import BaseCommand

from api.tasks import run_scrapers_nightly


class Command(BaseCommand):
    help = 'Runs all of the scrapers.  Good for setting up a development machine with new data.'

    def handle(self, *args, **options):
        self.stdout.write('Scraping Brigades and Projects from CfA website...')
        run_scrapers_nightly()  # running the nightly task pretty much covers it!
        self.stdout.write('Finished scraping brigades and projects!')
