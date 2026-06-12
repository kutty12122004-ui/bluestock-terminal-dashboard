import csv
from django.core.management.base import BaseCommand
from companies.models import Company

class Command(BaseCommand):
    help = 'Imports Nifty 100 enterprise data from dim_company.csv and normalizes metadata fields.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the dim_company.csv file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_count = 0
                updated_count = 0
                
                for row in reader:
                    # Use row.get() safely and aggressively strip whitespaces/hidden break characters (\n, \r)
                    ticker = row.get('symbol', '').replace('\r', '').replace('\n', '').strip()
                    name = row.get('company_name', '').replace('\r', '').replace('\n', '').strip()
                    industry = row.get('sector', '').replace('\r', '').replace('\n', '').strip()
                    
                    # Ensure structural data existence criteria are met before hit database layer
                    if ticker and name and industry:
                        obj, created = Company.objects.update_or_create(
                            symbol=ticker,
                            defaults={
                                'company_name': name,
                                'sector': industry,
                            }
                        )
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                        
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully processed dataset execution! Added {created_count} new entries, updated {updated_count}.'
                ))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Cannot find file at execution path: "{file_path}"'))