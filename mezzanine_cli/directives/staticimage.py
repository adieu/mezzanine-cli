from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst import directives
from django.contrib.staticfiles.storage import staticfiles_storage


class StaticImage(Image):
    def run(self):
        image = self.arguments[0]
        if not image.startswith('http'):
            self.arguments[0] = staticfiles_storage.url(image)
        return super(StaticImage, self).run()


directives.register_directive('staticimage', StaticImage)
