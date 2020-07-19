from django.core.management.base import BaseCommand
import os


class CustomBaseCommand(BaseCommand):
    default_file_name = None

    def add_arguments(self, parser):
        parser.add_argument(
                                '--file_name',
                                type=str,
                                help="Name of .xlsx file",
                                default=self.default_file_name
                            )

    def get_path_by_name(self, file_name, path):
        # TODO: Add validation in case file does not exist
        dir = os.path.dirname(path)
        abs_file_path = os.path.join(dir, file_name)
        return abs_file_path
