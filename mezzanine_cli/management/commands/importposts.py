import os
import sys
import fnmatch
from django.core.management.base import LabelCommand
from mezzanine.blog.models import BlogPost
from mezzanine_cli.parser import parse


class Command(LabelCommand):
    help = "Import blog posts from a specific folder."
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
                published_on = metadata.get('published_on', None)

                if title and slug and published_on:
                    try:
                        blog_post = BlogPost.objects.get(slug=slug)
                        blog_post.title = title
                        blog_post.publish_date = published_on
                        blog_post.content = content
                        blog_post.save()
                    except BlogPost.DoesNotExist:
                        BlogPost.objects.create(title=title, slug=slug, publish_date=published_on, content=content, user_id=1)
                else:
                    sys.stdout.write('ignoring %s\n' % rst_file)
