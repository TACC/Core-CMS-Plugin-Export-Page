from django.test import SimpleTestCase

from djangocms_tacc_export_page.html_blocks import html_to_blocks


class HtmlToBlocksTests(SimpleTestCase):
    def test_headings_and_list(self):
        html = '<h2>About</h2><p>Intro text.</p><ul><li>One</li><li>Two</li></ul>'
        blocks = html_to_blocks(html)
        kinds = [block.kind for block in blocks]
        self.assertEqual(kinds, ['heading2', 'paragraph', 'bullet', 'bullet'])
        self.assertEqual(blocks[0].text, 'About')

    def test_inline_phrasing_in_one_paragraph(self):
        html = (
            '<strong>Primary admonition.</strong> '
            'Appearance: admonition; context <code>primary</code>.'
        )
        blocks = html_to_blocks(html)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].kind, 'paragraph')
        self.assertIn('Primary admonition.', blocks[0].text)
        self.assertIn('primary', blocks[0].text)
        self.assertTrue(any(span.bold for span in blocks[0].runs))
        self.assertTrue(any(span.code for span in blocks[0].runs))

    def test_bold_and_link_in_paragraph(self):
        html = (
            '<p><strong>Primary alert.</strong> Body text. '
            '<a href="https://example.com/">Example link</a>.</p>'
        )
        blocks = html_to_blocks(html)
        self.assertEqual(len(blocks), 1)
        link_spans = [span for span in blocks[0].runs if span.url]
        self.assertEqual(len(link_spans), 1)
        self.assertEqual(link_spans[0].text, 'Example link')
        self.assertEqual(link_spans[0].url, 'https://example.com/')
        self.assertTrue(any(span.bold and span.text.startswith('Primary') for span in blocks[0].runs))
