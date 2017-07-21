from django.core.management.base import BaseCommand
from jsonapi import importers
import jsonapi.models


class Command(BaseCommand):
    help = 'Import terminology from files'

    def add_arguments(self, parser):
        parser.add_argument('file', help="File path")

    def handle(self, *args, **options):
        ifname = options['file']
        print('----> ' + ifname)
        # importers.import_from_csv(input_file, client_name, domain=domain, logger=logger)
