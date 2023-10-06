"""Generates a markdown file describing the examples apps"""

from textwrap import indent
from pathlib import Path

DOCS_PATH = Path(__file__).parent.parent / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
INDEX_MD_PATH = DOCS_PATH / "index.md"
THUMBNAILS_PATH = DOCS_PATH / "assets" / "thumbnails"


def run():
    """Generates a Gallery markdown file describing all the example

    Generates the text description looping the inside the EXAMPLES_PATH recursively

    - For each folder a header "## Folder Name" is added to the text
    - For each .py file of a header is added "### File Name" to the text as well as the content of the
    module docstring.
    """

    text = """
# Panel Chat Examples Gallery
"""
    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name == "examples":
            continue
        text += f"\n## {folder.name.title()}\n"

        # Loop through each .py file in the folder
        for file in sorted(folder.glob("*.py")):
            title = file.name.replace(".py", "").replace("_", " ").title()
            source_path = file.relative_to(EXAMPLES_PATH.parent)
            text += f"\n### {title}\n"

            with open(file) as f:
                docstring_lines = []
                in_docstring = False
                for line in f:
                    if in_docstring:
                        if '"""' in line:
                            break
                        docstring_lines.append(line.strip())
                    elif '"""' in line:
                        in_docstring = True

                thumbnail = THUMBNAILS_PATH / file.name.replace(".py", ".png")
                if thumbnail.exists():
                    thumbnail_str = (
                        "\n"
                        f'[<img src="../{thumbnail.relative_to(EXAMPLES_PATH.parent)}" '
                        f'alt="{title}" style="max-height: 400px; max-width: 100%;">]({source_path})'
                    )
                    docstring_lines.append(thumbnail_str)
                docstring_lines.append(
                    f"<details>\n"
                    f"<summary>Source code for <a href='{source_path.name}' target='_blank'>{source_path.name}</a></summary>\n"
                    f"```python\n"
                    f"{file.read_text()}\n"
                    f"```\n"
                    "</details>\n"
                )

                docstring = "\n".join(docstring_lines)

                text += f"\n{docstring}\n"

    # Write the text to the index.md file
    with open(INDEX_MD_PATH, "w") as f:
        f.write(text)


if __name__.startswith("__main__"):
    run()
