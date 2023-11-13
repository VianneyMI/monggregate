"""Module to test sync between readme.md and index.md files"""

from difflib import unified_diff


def test_sync():
    """Test sync between readme.md and index.md files"""

   

    with open('README.md', 'r') as readme_file:
        readme = readme_file.readlines()
    with open('docs/index.md', 'r') as index_file:
        index = index_file.readlines()
    assert readme == index, f"""README.md and docs/index.md files are not in sync.
    
    Diff:
        {list(unified_diff(readme, index, fromfile="readme.md", tofile="index.md", n=0))}
    """

if __name__ == '__main__':
    test_sync()
    print("Everything is in sync.")
 