from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Creates the buysell_items and buysell_cart tables directly in the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if tables exist
            cursor.execute("SHOW TABLES LIKE 'buysell_items'")
            if not cursor.fetchone():
                self.stdout.write('Creating buysell_items table...')
                cursor.execute('''
                CREATE TABLE `buysell_items` (
                    `item_id` varchar(20) NOT NULL PRIMARY KEY,
                    `product_name` varchar(100) NOT NULL,
                    `product_category` varchar(20) NOT NULL,
                    `product_description` longtext NOT NULL,
                    `price` integer UNSIGNED NOT NULL CHECK (`price` >= 0),
                    `photo` varchar(100) NOT NULL,
                    `availability_status` varchar(10) NOT NULL,
                    `usn_id` varchar(10) NOT NULL,
                    CONSTRAINT `buysell_items_usn_id_fk` FOREIGN KEY (`usn_id`) 
                    REFERENCES `login_users` (`usn`)
                )
                ''')
                self.stdout.write(self.style.SUCCESS('Successfully created buysell_items table'))
            else:
                self.stdout.write('buysell_items table already exists')

            cursor.execute("SHOW TABLES LIKE 'buysell_cart'")
            if not cursor.fetchone():
                self.stdout.write('Creating buysell_cart table...')
                cursor.execute('''
                CREATE TABLE `buysell_cart` (
                    `cart_id` varchar(50) NOT NULL PRIMARY KEY,
                    `date_added` date NOT NULL,
                    `usn_id` varchar(10) NOT NULL,
                    `item_id` varchar(20) NOT NULL,
                    CONSTRAINT `buysell_cart_usn_id_fk` FOREIGN KEY (`usn_id`) 
                    REFERENCES `login_users` (`usn`),
                    CONSTRAINT `buysell_cart_item_id_fk` FOREIGN KEY (`item_id`) 
                    REFERENCES `buysell_items` (`item_id`)
                )
                ''')
                self.stdout.write(self.style.SUCCESS('Successfully created buysell_cart table'))
            else:
                self.stdout.write('buysell_cart table already exists') 