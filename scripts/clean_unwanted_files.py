import os
import fnmatch

# Base directory: parent of this script's folder
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Patterns to delete everywhere except .bat (which has special rule)
file_patterns_to_remove = [
    '*vpp.bak*',
    '*vpp.lck*',
    '~$*',
    '*.tmp',
    '*.bak',
    '*.wbk',
    '*.asd',
    '*.lnk',
    '*.lock',
    '*.log',
    '*.ds_store',
    '*.sln.docstates',
    'Thumbs.db',
    'diff.path',
    '*.del',
    'catalog-v*.xml'
]


# Exception: do NOT delete *.bat if in /scripts folder
def is_bat_in_scripts_folder(file_path):
    rel_path = os.path.relpath(file_path, base_dir)
    parts = rel_path.replace("\\", "/").split('/')
    return 'scripts' in parts and rel_path.lower().endswith('.bat')


def should_delete(file_path, filename):
    # First, handle .bat exclusion rule
    if filename.lower().endswith('.bat'):
        return not is_bat_in_scripts_folder(file_path)

    # Other patterns
    for pattern in file_patterns_to_remove:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


# Find candidate files
files_to_delete = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if should_delete(file_path, file):
            files_to_delete.append(file_path)

# Display files
if not files_to_delete:
    print("No files matched the deletion criteria.")
else:
    print("The following files will be deleted:\n")
    for f in files_to_delete:
        print(f)

    print(f"\nTotal files that would be deleted: {len(files_to_delete)}")

    confirm = input("\nDo you want to proceed with deletion? [Y/N] (default: N): ").strip().lower()
    if confirm == "y":
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        print(f"\nTotal files deleted: {deleted_count}")
    else:
        print("\nDeletion cancelled.")
