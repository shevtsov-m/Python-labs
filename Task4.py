import hashlib

def generate_file_hashes(*file_paths):
    hashes = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as file:
                file_hash = hashlib.sha256()
                content = file.read()
                file_hash.update(content)
                hashes[file_path] = file_hash.hexdigest()
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except IOError:
            print(f"Error reading file {file_path}")

    return hashes

result = generate_file_hashes('test.txt', 'test2.txt')
print(result)