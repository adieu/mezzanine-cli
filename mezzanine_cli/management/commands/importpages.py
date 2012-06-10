import os
import sys
import fnmatch
from django.core.management.base import LabelCommand
from mezzanine.pages.models import RichTextPage
from mezzanine_cli.parser import parse


class Command(LabelCommand):
    help = "Import pages from a specific folder."
    args = "<folder>"
    label = 'folder'

    requires_model_validation = False

    def handle_label(self, folder, **options):
        for root, dirs, files in os.walk(folder):
            for filename in fnmatch.filter(files, '*.rst'):
                rst_file = os.path.join(root, filename)
                metadata, content = parse(rst_file)
                title = metadata.get('title', None)
                slug = metadata.get('slug', None)

                if title and slug:
                    try:
                        page = RichTextPage.objects.get(slug=slug)
                        page.title = title
                        page.content = content
                        page.save()
                    except RichTextPage.DoesNotExist:
                        RichTextPage.objects.create(title=title, slug=slug, content=content)
                else:
                    sys.stdout.write('ignoring %s\n' % rst_file)
