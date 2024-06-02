import json
import pytest
import subprocess
import os
import sys

# Add parent directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Sample JSON data for testing
directory_structure = {
    "name": "interpreter",
    "size": 4096,
    "time_modified": 1699957865,
    "permissions": "drwxr-xr-x",
    "contents": [
        {
            "name": ".gitignore",
            "size": 8911,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"},
        {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"},
        {
            "name": "README.md", "size": 83,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"},
        {
            "name": "ast", "size": 4096,
            "time_modified": 1699957739,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "go.mod",
                    "size": 225,
                    "time_modified": 1699957780,
                    "permissions": "-rw-r--r--"
                }
            ]
        },
        {
            "name": "lexer",
            "size": 4096,
            "time_modified": 1699957740,
            "permissions": "drwxr-xr-x"
        },
        {
            "name": "main.go",
            "size": 3456,
            "time_modified": 1699957790,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "parser",
            "size": 4096,
            "time_modified": 1699957740,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "token",
                    "size": 1234,
                    "time_modified": 1699957795,
                    "permissions": "-rw-r--r--"
                }
            ]
        }
    ]
}


# Write the sample JSON data to a file
@pytest.fixture(scope="module", autouse=True)
def setup_directory_json():
    with open('directory_test.json', 'w') as f:
        json.dump(directory_structure, f)
    yield
    os.remove('directory_test.json')


# Helper function to run the pyls script
def run_pyls(args):
    result = subprocess.run(['python3', 'pyls.py'] + args, capture_output=True, text=True)
    print(f"Running pyls with argument: {args}")
    print(f"Output:\n{result.stdout.strip()}")
    print(f"Errors:\n{result.stderr.strip()}")
    return result.stdout.strip(), result.stderr.strip()


def test_ls_default():
    expected_output = ('/LICENSE\n/README.md\n/ast\n/go.mod\n/lexer\n/main.go\n/parser\n/token', '')
    assert run_pyls([]) == expected_output


def test_ls_all():
    expected_output = ('/.gitignore\n/LICENSE\n/README.md\n/ast\n/go.mod\n/lexer\n/main.go\n/parser\n/token', '')
    assert run_pyls(['-A']) == expected_output


def test_ls_recursive():
    expected_output = ('/LICENSE\n/README.md\n/ast\n    ast/go.mod\n    ast/ast.go\n/go.mod\n/lexer\n    lexer/lexer_test.go\n    lexer/go.mod\n    lexer/lexer.go\n/main.go\n/parser\n    parser/parser_test.go\n    parser/parser.go\n    parser/go.mod\n/token\n    token/token.go\n    token/go.mod', '')
    assert run_pyls(['-R']) == expected_output


def test_ls_reverse():
    expected_output = ('/token\n/parser\n/main.go\n/lexer\n/go.mod\n/ast\n/README.md\n/LICENSE', '')
    assert run_pyls(['-r']) == expected_output


def test_ls_sort_time():
    expected_output = ('/LICENSE\n/README.md\n/go.mod\n/main.go\n/token\n/lexer\n/ast\n/parser', '')
    assert run_pyls(['-t']) == expected_output


def test_ls_filter_file():
    expected_output = ('/LICENSE\n/README.md\n/go.mod\n/main.go', '')
    assert run_pyls(['--filter=file']) == expected_output


def test_ls_filter_dir():
    expected_output = ('/ast\n/lexer\n/parser\n/token', '')
    assert run_pyls(['--filter=dir']) == expected_output








