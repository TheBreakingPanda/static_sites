from blocktypes import BlockType, block_to_block_type
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block):
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]
    code_leaf = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_leaf])


def quote_to_html_node(block):
    lines = [line.removeprefix(">").strip() for line in block.split("\n")]
    content = " ".join(lines)
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for i, line in enumerate(block.split("\n")):
        prefix = f"{i + 1}. "
        text = line[len(prefix) :]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)
