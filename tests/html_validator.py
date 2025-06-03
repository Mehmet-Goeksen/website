import os
import sys

try:
    import html5lib
    from xml.etree import ElementTree
except ImportError:
    sys.stderr.write(
        "html5lib is required for this script. Install with 'pip install html5lib'\n"
    )
    sys.exit(1)


def validate_file(path: str):
    parser = html5lib.HTMLParser(strict=True)
    with open(path, "r", encoding="utf-8") as f:
        document = parser.parse(f)

    errors = []

    html_tags = document.findall('.//{http://www.w3.org/1999/xhtml}html')
    if len(html_tags) != 1:
        errors.append(f"Expected 1 <html> tag, found {len(html_tags)}")

    head_tags = document.findall('.//{http://www.w3.org/1999/xhtml}head')
    if len(head_tags) != 1:
        errors.append(f"Expected 1 <head> tag, found {len(head_tags)}")

    body_tags = document.findall('.//{http://www.w3.org/1999/xhtml}body')
    if len(body_tags) != 1:
        errors.append(f"Expected 1 <body> tag, found {len(body_tags)}")

    if head_tags:
        title_tags = head_tags[0].findall('.//{http://www.w3.org/1999/xhtml}title')
        if len(title_tags) < 1:
            errors.append("Missing <title> element")
        elif len(title_tags) > 1:
            errors.append(f"Duplicate <title> elements: {len(title_tags)}")

    return errors


def main(root: str):
    html_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))

    any_errors = False
    for path in html_files:
        errs = validate_file(path)
        if errs:
            any_errors = True
            print(f"Errors in {path}:")
            for err in errs:
                print(f"  - {err}")

    if not any_errors:
        print("All HTML files passed validation")
    return 1 if any_errors else 0


if __name__ == '__main__':
    sys.exit(main('.'))
