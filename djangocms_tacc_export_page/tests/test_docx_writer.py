import zipfile
from io import BytesIO

from django.test import SimpleTestCase

from djangocms_tacc_export_page.document import Block, InlineSpan, PageDocument
from djangocms_tacc_export_page.docx_writer import write_page_document


class DocxWriterTests(SimpleTestCase):
    def test_writes_docx_bytes(self):
        document = PageDocument(
            title='Test Page',
            slug='test',
            page_url='https://example.com/test/',
            blocks=[
                Block('heading2', 'Section'),
                Block('paragraph', 'Body copy.'),
            ],
        )
        payload = write_page_document(document)
        self.assertTrue(payload.startswith(b'PK'))
        self.assertGreater(len(payload), 500)

    def test_writes_bold_and_hyperlink_runs(self):
        document = PageDocument(
            title='Test Page',
            blocks=[
                Block(
                    'paragraph',
                    'Primary alert. Example link.',
                    runs=(
                        InlineSpan('Primary alert.', bold=True),
                        InlineSpan(' Example '),
                        InlineSpan('link', url='https://example.com/'),
                        InlineSpan('.'),
                    ),
                ),
            ],
        )
        payload = write_page_document(document)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            xml = archive.read('word/document.xml').decode('utf-8')
            rels = archive.read('word/_rels/document.xml.rels').decode('utf-8')
        self.assertIn('w:b', xml)
        self.assertIn('w:hyperlink', xml)
        self.assertIn('https://example.com/', rels)
