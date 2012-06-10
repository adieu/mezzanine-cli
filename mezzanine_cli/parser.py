import docutils
import docutils.core
import mezzanine_cli.directives


def get_publisher(filename):
    extra_params = {'initial_header_level': '2'}
    pub = docutils.core.Publisher(
            destination_class=docutils.io.StringOutput)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.process_programmatic_settings(None, extra_params, None)
    pub.set_source(source_path=filename)
    pub.publish()
    return pub


def parse_metadata(document):
    """Return the dict containing document metadata"""
    output = {}
    for docinfo in document.traverse(docutils.nodes.docinfo):
        for element in docinfo.children:
            if element.tagname == 'field':  # custom fields (e.g. summary)
                name_elem, body_elem = element.children
                name = name_elem.astext()
                value = body_elem.astext()
            else:  # standard fields (e.g. address)
                name = element.tagname
                value = element.astext()
            name = name.lower()

            output[name] = value
    return output


def parse(filename):
    pub = get_publisher(filename)
    metadata = parse_metadata(pub.document)
    content = pub.writer.parts.get('body')
    return metadata, content
