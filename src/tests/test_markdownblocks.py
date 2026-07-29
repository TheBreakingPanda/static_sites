import unittest

from markdownblocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_heading(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is a paragraph




This is another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is another paragraph",
            ],
        )

    def test_markdown_to_blocks_strips_whitespace(self):
        md = "   This has leading and trailing spaces   \n\n  So does this block  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This has leading and trailing spaces",
                "So does this block",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text"])

    def test_markdown_to_blocks_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   \n\n  "), [])


if __name__ == "__main__":
    unittest.main()
