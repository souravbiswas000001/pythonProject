Python List Directory Contents (pyls)

pyls is a Python command-line tool that lists information about files and directories in the specified directory. It provides options to customize the output format, sort order, and filter criteria.

Features:

List directory contents in various formats: short, long, recursive.
Sort files by modification time.
Filter files and directories based on type (file or directory).
Support for relative and absolute paths.
Customizable output format.
Installation

Clone the repository:
git clone https://github.com/souravbiswas000001/pyls.git

Navigate to the project directory:
cd pyls

Install the project dependencies:
pip install -r requirements.txt

Run pyls using the provided command-line interface:

python -m pyls [options] [directory]

-A, --all: Show hidden files.
-R, --recursive: List subdirectories recursively.
-l: Use a long listing format.
-t, --sort-time: Sort by time modified (oldest first).
-r, --reverse: Reverse the order of the output.
--filter: Filter the output based on type (file or dir).
Directory: Directory to list. If not specified, the current directory is used.

Examples:

List all files and directories in the current directory:
python -m pyls

List all files and directories in the current directory recursively:
python -m pyls -R

List all files in the current directory with a long listing format:
python -m pyls -l

List all files in the current directory sorted by modification time:
python -m pyls -t

List all directories in the current directory:
python -m pyls --filter=dir
