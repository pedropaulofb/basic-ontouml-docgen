import json
import argparse
from pathlib import Path

def load_json(input_path):
    """
    Loads a JSON file from the specified path and returns the parsed content.

    Args:
        input_path (str or Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON content as a dictionary.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def index_diagrams_by_owner(diagrams):
    """
    Indexes diagrams by their owner's ID, organizing them into a dictionary.

    Args:
        diagrams (list): A list of diagrams, each containing an 'owner' key with an 'id'.

    Returns:
        dict: A dictionary where the key is the owner ID and the value is a list of diagrams owned by that ID.
    """
    diagrams_by_owner = {}
    for diagram in diagrams:
        owner_id = diagram["owner"]["id"]
        diagrams_by_owner.setdefault(owner_id, []).append(diagram)
    return diagrams_by_owner

def find_image_for_element(element_name, images_folder):
    """
    Searches for an image file corresponding to an element by its name in the specified folder.

    Args:
        element_name (str): The name of the element to find the image for.
        images_folder (str or Path): Path to the folder containing images.

    Returns:
        Path or None: The path to the image file if found, otherwise None.
    """
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
    """
    Processes a package and generates the corresponding Markdown lines for the package and its contents.

    Args:
        pkg (dict): A dictionary representing a package, which may contain a 'name', 'description', 'id',
                    and other metadata.
        diagrams_by_owner (dict): A dictionary of diagrams indexed by owner ID.
        images_folder (str or Path): Path to the folder containing images for diagrams and packages.
        level (int): The Markdown heading level to use for this package.

    Returns:
        list: A list of strings representing the Markdown content for this package and its contents.
    """
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

    # Process diagrams associated with the package
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

    # Recursively process sub-packages
    contents = pkg.get("contents") or []
    for content in contents:
        if content["type"] == "Package":
            lines.extend(process_package(content, diagrams_by_owner, images_folder, level=level + 1))

    return lines

def generate_markdown(data, images_folder=None):
    """
    Generates the complete Markdown documentation from the given data.

    Args:
        data (dict): The data representing the OntoUML model, including information about packages and diagrams.
        images_folder (str or Path, optional): Path to the folder containing images to include in the documentation.

    Returns:
        str: The generated Markdown documentation as a string.
    """
    lines = [f"# {data['name']}", ""]

    model = data.get("model", {})
    contents = model.get("contents") or []

    diagrams_by_owner = index_diagrams_by_owner(data.get("diagrams", []))

    # Process each top-level package
    for top_level_pkg in contents:
        lines.extend(process_package(top_level_pkg, diagrams_by_owner, images_folder))

    return "\n".join(lines)

def main():
    """
    The main entry point of the script. It parses command-line arguments, loads the OntoUML JSON data,
    generates Markdown documentation, and writes it to the specified output file.
    """
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
    print(f"Documentation written to: {args.output_md}")

if __name__ == "__main__":
    main()
