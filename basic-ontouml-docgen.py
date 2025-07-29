import json
import argparse
from pathlib import Path
import os

def load_json(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def index_diagrams_by_owner(diagrams):
    diagrams_by_owner = {}
    for diagram in diagrams:
        owner_id = diagram["owner"]["id"]
        diagrams_by_owner.setdefault(owner_id, []).append(diagram)
    return diagrams_by_owner

def find_image_for_element(element_name, images_folder):
    if not images_folder:  # Ensure images_folder is valid
        return None

    # Check for a match in the images folder
    image_extensions = ['.png', '.jpg', '.jpeg']
    for ext in image_extensions:
        image_path = Path(images_folder) / f"{element_name}{ext}"
        if image_path.exists():
            return image_path
    return None

def process_package(pkg, diagrams_by_owner, images_folder, level=2):
    heading_prefix = "#" * level
    lines = [f"{heading_prefix} {pkg['name']}", ""]

    if pkg.get("description"):
        lines.append(str(pkg["description"]))
        lines.append("")

    # Check if there is a matching image for the package
    image = find_image_for_element(pkg["name"], images_folder)
    if image:
        relative_image_path = Path(images_folder) / image.name  # Directly use the user-provided images_folder
        lines.append(f"![{pkg['name']}]({relative_image_path})")
        lines.append("")

    for diagram in diagrams_by_owner.get(pkg["id"], []):
        lines.append(f"{'#' * (level + 1)} {diagram['name']}")
        lines.append("")
        lines.append(str(diagram.get("description") or ""))
        lines.append("")

        # Check if there is a matching image for the diagram
        image = find_image_for_element(diagram['name'], images_folder)
        if image:
            relative_image_path = Path(images_folder) / image.name  # Directly use the user-provided images_folder
            lines.append(f"![{diagram['name']}]({relative_image_path})")
            lines.append("")

    contents = pkg.get("contents") or []
    for content in contents:
        if content["type"] == "Package":
            lines.extend(process_package(content, diagrams_by_owner, images_folder, level=level + 1))

    return lines

def generate_markdown(data, images_folder=None):
    lines = [f"# {data['name']}", ""]

    model = data.get("model", {})
    contents = model.get("contents") or []

    diagrams_by_owner = index_diagrams_by_owner(data.get("diagrams", []))

    for top_level_pkg in contents:
        lines.extend(process_package(top_level_pkg, diagrams_by_owner, images_folder))

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation from OntoUML JSON export.")
    parser.add_argument("input_json", help="Path to the OntoUML JSON file")
    parser.add_argument("output_md", help="Path to write the Markdown output file")
    parser.add_argument("images_folder", nargs="?", help="Optional folder containing images to include in the documentation", default=None)

    args = parser.parse_args()
    data = load_json(args.input_json)

    # Ensure images_folder is provided or set to None if not passed
    images_folder = args.images_folder if args.images_folder else None

    markdown_output = generate_markdown(data, images_folder=images_folder)

    Path(args.output_md).write_text(markdown_output, encoding="utf-8")
    print(f"✅ Documentation written to: {args.output_md}")

if __name__ == "__main__":
    main()
