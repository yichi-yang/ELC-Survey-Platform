import markdown
from markdown.treeprocessors import Treeprocessor
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from rest_framework.compat import (
    HEADERID_EXT_PATH, LEVEL_PARAM, md_filter_add_syntax_highlight
)
from rest_framework.utils import formatting

# https://stackoverflow.com/a/53454455

TABLE_EXTENSION_PATH = 'markdown.extensions.tables'
FENCED_CODE_EXTENSION_PATH = 'markdown.extensions.fenced_code'


class MakeshiftTableTreeprocessor(Treeprocessor):
    """ Adds Bootstrap style class name to table tags. """
    # https://getbootstrap.com/docs/4.0/content/tables/

    def run(self, root):
        for table in root.findall('.//table'):
            table.set("class", "table")
            for col_header in table.findall('./thead/tr/th'):
                col_header.set("scope", "col")
            for col_header in table.findall('./tbody/tr/th'):
                col_header.set("scope", "row")


def md_filter_set_table_class(md):
    md.treeprocessors.register(
        MakeshiftTableTreeprocessor(), 'bootstrap-table', 30)


def _apply_markdown(text):
    extensions = [
        HEADERID_EXT_PATH,
        TABLE_EXTENSION_PATH,
        FENCED_CODE_EXTENSION_PATH
    ]
    extension_configs = {
        HEADERID_EXT_PATH: {
            LEVEL_PARAM: '2'
        }
    }
    md = markdown.Markdown(
        extensions=extensions, extension_configs=extension_configs
    )
    md_filter_add_syntax_highlight(md)
    md_filter_set_table_class(md)
    return md.convert(text)


def get_view_description(view_cls, html=False):
    description = view_cls.__doc__ or ''
    description = formatting.dedent(smart_str(description))

    if html:
        return mark_safe(_apply_markdown(description))
    return description
