from django.test import SimpleTestCase

from djangocms_tacc_page_export.html_blocks import html_to_blocks


class HtmlToBlocksTests(SimpleTestCase):
    def test_headings_and_list(self):
        html = '<h2>About</h2><p>Intro text.</p><ul><li>One</li><li>Two</li></ul>'
        blocks = html_to_blocks(html)
        kinds = [block.kind for block in blocks]
        self.assertEqual(kinds, ['heading2', 'paragraph', 'bullet', 'bullet'])
        self.assertEqual(blocks[0].text, 'About')
