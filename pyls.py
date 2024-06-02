import argparse
import json
import time
import sys


def format_time(epoch_time):
    """Convert epoch time to a human-readable format."""
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(epoch_time))


def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def list_directory(directory, show_all=False, recursive=False, long_format=False, sort_by_time=False, reverse=False, filter_by=None, indent=0, path=""):
    """Print directory contents based on the specified options."""
    prefix = ' ' * (indent * 4)
    contents = directory.get('contents', [])

    # Sort by time_modified if sort_by_time is True, then reverse if reverse is True
    if sort_by_time:
        contents.sort(key=lambda x: x['time_modified'])
    if reverse:
        contents.reverse()

    for item in contents:
        # Skip hidden files unless show_all is True
        if not show_all and item['name'].startswith('.'):
            continue

        # Apply filter if filter_by is specified
        if filter_by == 'file' and 'contents' in item:
            continue
        if filter_by == 'dir' and 'contents' not in item:
            continue

        if long_format:
            size_str = human_readable_size(item['size'])
            print(f"{prefix}{item['permissions']} {size_str:>9} {format_time(item['time_modified'])} {path}/{item['name']}")
        else:
            # Remove the starting '/' character from the path
            print(f"{prefix}{path[1:]}/{item['name']}")

        # Recursively list contents if recursive and the item is a directory
        if recursive and 'contents' in item:
            list_directory(item, show_all, recursive, long_format, sort_by_time, reverse, filter_by, indent + 1, f"{path}/{item['name']}")

def find_directory_or_file(directory, path):
    """Find a subdirectory or file given a path."""
    if path in ['', '.']:
        return directory, True  # Root directory
    parts = path.split('/')
    current = directory
    for part in parts:
        for item in current.get('contents', []):
            if item['name'] == part:
                if 'contents' in item:
                    current = item
                else:
                    return item, False  # Return file and not a directory
                break
        else:
            print(f"error: cannot access '{path}': No such file or directory")
            sys.exit(1)
    return current, True  # Return directory and not a file


class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, choices=None, **kwargs):
        self._choices = choices
        super().__init__(*args, **kwargs)

    def error(self, message):
        if 'invalid choice' in message:
            valid_choices = ', '.join([repr(choice) for choice in self._choices])
            invalid_choice = message.split(': ')[-1].split(' ')[0]
            message = f"error: '{invalid_choice}' is not a valid filter criteria. Available filters are {valid_choices}"
        super().error(message)


def main():
    parser = CustomArgumentParser(description="List information about the FILEs (the current directory by default).", choices=['file', 'dir'])
    parser.add_argument('directory', nargs='?', default='', help="directory to list")
    parser.add_argument('-A', '--all', action='store_true', help="do not ignore entries starting with .")
    parser.add_argument('-R', '--recursive', action='store_true', help="list subdirectories recursively")
    parser.add_argument('-l', action='store_true', help="use a long listing format")
    parser.add_argument('-t', '--sort-time', action='store_true', help="sort by time modified (oldest first)")
    parser.add_argument('-r', '--reverse', action='store_true', help="reverse the order of the output")
    parser.add_argument('--filter', choices=['file', 'dir'], help="filter the output based on type (file or dir)")

    args = parser.parse_args()

    # Load the JSON file
    with open('directory.json', 'r') as file:
        directory_structure = json.load(file)

    # Handle relative paths
    target, is_dir = find_directory_or_file(directory_structure, args.directory)

    # Print the directory contents based on the arguments
    if is_dir:
        list_directory(target, show_all=args.all, recursive=args.recursive, long_format=args.l,
                       sort_by_time=args.sort_time, reverse=args.reverse, filter_by=args.filter, path=args.directory)
    else:
        if args.filter and args.filter != 'file':
            print(f"error: '{args.directory}' is not a directory")
            sys.exit(1)
        if args.l:
            size_str = human_readable_size(target['size'])
            print(f"{target['permissions']} {size_str:>9} {format_time(target['time_modified'])} ./{args.directory}")
        else:
            print(f"./{args.directory}")


if __name__ == "__main__":
    main()