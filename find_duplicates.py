import os
import hashlib
import argparse

def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except (OSError, IOError):
        return None
    return hash_md5.hexdigest()

def find_duplicates(root_dir, skip_dirs=None):
    """Find duplicate files in a directory."""
    if skip_dirs is None:
        skip_dirs = {'.git', '.venv', '__pycache__', '.gemini', '.agent', 'node_modules', 'dist', 'build'}
    
    skip_files = {'__init__.py', 'duplicates.txt', 'duplicates_utf8.txt', 'find_duplicates.py'}
    
    hashes = {}
    duplicates = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        for filename in filenames:
            if filename in skip_files:
                continue
            file_path = os.path.join(dirpath, filename)
            file_hash = get_file_hash(file_path)
            
            if file_hash:
                if file_hash in hashes:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hashes[file_hash]]
                    duplicates[file_hash].append(file_path)
                else:
                    hashes[file_hash] = file_path
    
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Find and remove duplicate files.")
    parser.add_argument("directory", help="Directory to search for duplicates")
    parser.add_argument("--delete", action="store_true", help="Delete duplicate files")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    print(f"Searching for duplicates in: {root_dir}")
    
    duplicates = find_duplicates(root_dir)
    
    if not duplicates:
        print("No duplicate files found.")
        return

    total_duplicates = 0
    for file_hash, paths in duplicates.items():
        print(f"\nDuplicate group (Hash: {file_hash}):")
        # Keep the first one, delete the rest
        original = paths[0]
        to_delete = paths[1:]
        print(f"  [KEEP] {original}")
        for path in to_delete:
            total_duplicates += 1
            if args.delete:
                try:
                    os.remove(path)
                    print(f"  [DELETED] {path}")
                except OSError as e:
                    print(f"  [ERROR] Could not delete {path}: {e}")
            else:
                print(f"  [DUPLICATE] {path}")

    if not args.delete:
        print(f"\nFound {total_duplicates} duplicate files. Run with --delete to remove them.")
    else:
        print(f"\nDeleted {total_duplicates} duplicate files.")

if __name__ == "__main__":
    main()
