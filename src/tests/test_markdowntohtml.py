import unittest

from markdownblocks import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is an h1\n\n## This is an h2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><h2>This is an h2</h2></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "### Heading with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading with <b>bold</b> text</h3></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n> that spans two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- item one\n- item two with **bold**\n- item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two with <b>bold</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first item\n2. second item with _italic_\n3. third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item with <i>italic</i></li><li>third item</li></ol></div>",
        )

    def test_all_block_types_together(self):
        md = """
# Heading

This is a paragraph with a [link](https://boot.dev)

> A quote block

- unordered one
- unordered two

1. ordered one
2. ordered two

```
raw code here
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            '<p>This is a paragraph with a <a href="https://boot.dev">link</a></p>'
            "<blockquote>A quote block</blockquote>"
            "<ul><li>unordered one</li><li>unordered two</li></ul>"
            "<ol><li>ordered one</li><li>ordered two</li></ol>"
            "<pre><code>raw code here\n</code></pre>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
