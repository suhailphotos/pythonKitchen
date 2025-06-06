import os
from pathlib import Path

SKIP_EXTS = {'.env'}
SKIP_NAMES = {'.env'}
SKIP_TREE_FILES = {'__pycache__', 'dist', '.git'}

def build_tree(root):
    lines = []
    dir_count = 0
    file_count = 0

    def walk(dir_path, prefix=""):
        nonlocal dir_count, file_count
        entries = sorted(os.listdir(dir_path))
        entries = [e for e in entries if e not in SKIP_NAMES]
        for idx, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            is_last = (idx == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            sub_prefix = "    " if is_last else "│   "
            if os.path.isdir(path):
                if entry in {'.git', 'dist'}:
                    lines.append(f"{prefix}{connector}{entry}")
                    lines.append(f"{prefix}{sub_prefix}// * files hidden for brevity")
                    dir_count += 1
                    continue
                if entry == '__pycache__':
                    lines.append(f"{prefix}{connector}{entry}")
                    lines.append(f"{prefix}{sub_prefix}// * files hidden for brevity")
                    dir_count += 1
                    continue
                lines.append(f"{prefix}{connector}{entry}")
                dir_count += 1
                walk(path, prefix + sub_prefix)
            else:
                if entry in SKIP_NAMES or any(entry.endswith(ext) for ext in SKIP_EXTS):
                    continue
                lines.append(f"{prefix}{connector}{entry}")
                file_count += 1
    lines.append(str(root))
    walk(str(root))
    lines.append(f"\n{dir_count} directories, {file_count} files\n")
    return "\n".join(lines)

def dump_code_files(root):
    blocks = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Remove skipped folders from traversal
        dirnames[:] = [d for d in dirnames if d not in SKIP_TREE_FILES and not d.startswith('.')]
        for fname in filenames:
            if fname in SKIP_NAMES or fname.startswith('.'):
                continue
            ext = Path(fname).suffix.lower()
            if ext not in ('.py', '.json'):
                continue
            # Skip files in .git or dist folders
            rel_dir = Path(dirpath).relative_to(root)
            if any(part in {'.git', 'dist'} for part in rel_dir.parts):
                continue
            rel_path = Path(dirpath, fname).relative_to(root)
            # Only print __init__.py if non-empty
            if fname == '__init__.py':
                try:
                    with open(os.path.join(dirpath, fname), encoding="utf-8", errors="replace") as f:
                        content = f.read().strip()
                except Exception:
                    continue
                if not content:
                    continue
            else:
                try:
                    with open(os.path.join(dirpath, fname), encoding="utf-8", errors="replace") as f:
                        content = f.read().strip()
                except Exception:
                    continue
            lang = "python" if ext == ".py" else "json"
            blocks.append(f"path: {rel_path}")
            blocks.append(f"```{lang}\n{content}\n```")
    return "\n\n".join(blocks)

def export_project(root_path: str, output_path: str = None):
    """
    Generates a combined tree/code listing for the given root_path.
    If output_path is given, writes to that file. Otherwise, prints to stdout.
    """
    root = Path(root_path).resolve()
    text = []
    text.append(build_tree(root))
    text.append(dump_code_files(root))
    full = "\n\n".join(text)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full)
        print(f"Exported to {output_path}")
    else:
        print(full)
