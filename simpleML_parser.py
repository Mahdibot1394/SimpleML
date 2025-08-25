import re

class SimpleMLParser:
    def __init__(self, markup):
        self.markup = markup

    def parse(self):
        # Define tag to HTML mapping
        tag_map = {
            'title': lambda x: f"<title>{x}</title>",
            'heading': lambda x: f"<h1>{x}</h1>",
            'heading2': lambda x: f"<h2>{x}</h2>",
            'heading3': lambda x: f"<h3>{x}</h3>",
            'heading4': lambda x: f"<h4>{x}</h4>",
            'heading5': lambda x: f"<h5>{x}</h5>",
            'heading6': lambda x: f"<h6>{x}</h6>",
            'text': lambda x: f"<p>{x}</p>",
            'code': lambda x: f"<pre><code>{x}</code></pre>",
        }
        # Pattern to match <tag>content</tag>
        pattern = re.compile(r"((\w+))(.*?)(e \1)", re.DOTALL)
        html_output = self.markup
        # Replace each SimpleML tag with corresponding HTML
        for match in pattern.finditer(self.markup):
            tag, content = match.groups()
            if tag in tag_map:
                html = tag_map[tag](content.strip())
                html_output = html_output.replace(match.group(0), html)
        return html_output

if __name__ == "__main__":
    simpleml_doc = """
    (heading)Hello World!(e heading)
    """
    parser = SimpleMLParser(simpleml_doc)
    html_result = parser.parse()
    print(html_result)