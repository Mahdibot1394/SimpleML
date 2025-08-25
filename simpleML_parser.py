import re

class SimpleMLParser:
    def __init__(self, markup):
        self.markup = markup

    def parse(self):
        # Tag to HTML mapping (20 tags)
        tag_map = {
            'title': lambda x: f"<h1>{x}</h1>",
            'heading': lambda x: f"<h2>{x}</h2>",
            'subheading': lambda x: f"<h3>{x}</h3>",
            'text': lambda x: f"<p>{x}</p>",
            'bold': lambda x: f"<b>{x}</b>",
            'italic': lambda x: f"<i>{x}</i>",
            'underline': lambda x: f"<u>{x}</u>",
            'strike': lambda x: f"<del>{x}</del>",
            'list': lambda x: f"<ul>{''.join([f'<li>{i.strip()}</li>' for i in x.split('|')])}</ul>",
            'numbered': lambda x: f"<ol>{''.join([f'<li>{i.strip()}</li>' for i in x.split('|')])}</ol>",
            'quote': lambda x: f"<blockquote>{x}</blockquote>",
            'link': lambda x: f"<a href='{x.split('|')[0]}'>{x.split('|')[1]}</a>" if '|' in x else x,
            'image': lambda x: f"<img src='{x.split('|')[0]}' alt='{x.split('|')[1] if '|' in x else ''}' />",
            'code': lambda x: f"<pre><code>{x}</code></pre>",
            'inlinecode': lambda x: f"<code>{x}</code>",
            'hr': lambda x: "<hr />",
            'table': lambda x: "<table>" + ''.join(["<tr>" + ''.join([f"<td>{cell.strip()}</td>" for cell in row.split(';')]) + "</tr>" for row in x.split('|')]) + "</table>",
            'center': lambda x: f"<div style='text-align:center'>{x}</div>",
            'right': lambda x: f"<div style='text-align:right'>{x}</div>",
            'left': lambda x: f"<div style='text-align:left'>{x}</div>",
        }
        # Pattern to match (tag)content(end tag)
        pattern = re.compile(r"\((\w+)\)(.*?)\(end \1\)", re.DOTALL)
        html_output = self.markup
        # Replace each tag with HTML
        for match in pattern.finditer(self.markup):
            tag, content = match.groups()
            if tag in tag_map:
                html = tag_map[tag](content.strip())
                html_output = html_output.replace(match.group(0), html)
        return html_output

if __name__ == "__main__":
    simpleml_doc = """
    (title)My Document(end title)
    (heading)Main Section(end heading)
    (subheading)Subsection(end subheading)
    (text)This is some text in a paragraph.(end text)
    (bold)This text is bold(end bold)
    (italic)This text is italic(end italic)
    (underline)Underline me(end underline)
    (strike)Strike this out(end strike)
    (list)Item 1|Item 2|Item 3(end list)
    (numbered)First|Second|Third(end numbered)
    (quote)This is a quoted block(end quote)
    (link)https://github.com|GitHub(end link)
    (image)https://via.placeholder.com/100|Placeholder Image(end image)
    (code)print("Hello, World!")(end code)
    (inlinecode)x = 42(end inlinecode)
    (hr)(end hr)
    (table)Name;Age|Alice;30|Bob;25(end table)
    (center)Centered text(end center)
    (right)Right aligned text(end right)
    (left)Left aligned text(end left)
    """
    parser = SimpleMLParser(simpleml_doc)
    html_result = parser.parse()
    print(html_result)