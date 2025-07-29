# basic-ontouml-docgen

**A Python script to generate Markdown documentation from OntoUML JSON exports, with optional image inclusion.**

## Overview

`basic-ontouml-docgen.py` is a Python script designed to automate the generation of Markdown documentation for OntoUML models. The script parses OntoUML JSON exports, extracts metadata, and descriptions to generate a structured and readable Markdown file. It also allows for the inclusion of diagrams by linking images stored in a specified folder. This tool is ideal for OntoUML practitioners, ontology engineers, and developers who need to document their models efficiently.

## Features

* **Automatic Extraction**: Extracts class names, stereotypes, attributes, descriptions, and diagrams from OntoUML JSON exports.
* **Markdown Generation**: Converts extracted data into a structured Markdown format for documentation.
* **Image Integration**: Optionally links images for elements (e.g., classes, packages, diagrams) from a specified folder.
* **Customizable Output**: Allows customization of the structure and content of the generated Markdown file.
* **Command-Line Interface**: Simple CLI for easy execution and integration into workflows.

## Requirements

* Python 3.x
* No additional external dependencies. Standard libraries used include `json`, `argparse`, `pathlib`, and `os`.

## Usage

Run the script using the following command:

```
python basic-ontouml-docgen.py <path_to_ontouml_json> <output_markdown_file> [<images_folder>]
```

* `<path_to_ontouml_json>`: Path to the OntoUML JSON export file.
* `<output_markdown_file>`: Desired output Markdown file name.
* `<images_folder>` *(optional)*: Path to the folder containing images that correspond to elements in the OntoUML model. Images should be named after the elements (e.g., `class_name.png` for a class diagram).

Example:

```
python basic-ontouml-docgen.py model.json documentation.md ./images
```

This command generates a `documentation.md` file from `model.json` and includes images found in the `./images` folder.

## Script Details

1. **Load JSON**: The script loads the OntoUML JSON export from the specified path using the `load_json` function.
2. **Index Diagrams by Owner**: The `index_diagrams_by_owner` function organizes diagrams by their owner element (e.g., packages or classes).
3. **Find Images**: The script looks for corresponding images in the `images_folder` directory using the `find_image_for_element` function. It checks for image files with the extensions `.png`, `.jpg`, or `.jpeg`.
4. **Process Packages and Diagrams**: The script processes each package and its associated diagrams, generating appropriate Markdown headers, descriptions, and image links. This is handled by the `process_package` function. The function recursively handles sub-packages.
5. **Generate Markdown**: The script compiles the extracted data into a Markdown file using the `generate_markdown` function, linking images where applicable.
6. **Markdown Formatting**: For each package and diagram, the script applies appropriate heading levels based on their hierarchical structure and appends descriptions and images where available.

## Example Output

The generated Markdown file will include:

* **Headers** for packages and diagrams, formatted with Markdown syntax. The hierarchy is reflected with different heading levels for packages and their contents.
* **Descriptions** of packages, diagrams, and elements where provided in the OntoUML JSON.
* **Images** corresponding to the elements, if found in the specified image folder. Image links are relative to the provided image folder path.

## License

This project is licensed under the Apache License, Version 2.0.

You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
