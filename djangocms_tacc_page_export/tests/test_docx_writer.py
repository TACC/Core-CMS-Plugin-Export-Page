from django.test import SimpleTestCase

from djangocms_tacc_page_export.document import Block, PageDocument
from djangocms_tacc_page_export.docx_writer import write_page_document


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
