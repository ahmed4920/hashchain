import hashlib
import os
import heapq

def calculate_file_hash(filepath, hash_algorithm='sha1'):
    try:
        with open(filepath, 'rb') as f:
            if hash_algorithm == 'md5':
                hasher = hashlib.md5()
            elif hash_algorithm == 'sha1':
                hasher = hashlib.sha1()
            else:
                raise ValueError("Invalid hash algorithm. Use 'md5' or 'sha1'.")

            while chunk := f.read(4096):
                hasher.update(chunk)
            return hasher.hexdigest()
    except FileNotFoundError:
        return None  

def calculate_top_hash(file_paths, hash_algorithm='sha1'):
    file_hashes = []
    for filepath in file_paths:
        file_hash = calculate_file_hash(filepath, hash_algorithm)
        if file_hash is not None:
            file_hashes.append(file_hash)

    if not file_hashes:
        return None  

    combined_hash_input = ''.join(sorted(file_hashes)).encode('utf-8')  

    if hash_algorithm == 'md5':
        combined_hasher = hashlib.md5(combined_hash_input)
    elif hash_algorithm == 'sha1':
        combined_hasher = hashlib.sha1(combined_hash_input)
    else:
        raise ValueError("Invalid hash algorithm. Use 'md5' or 'sha1'.")

    return combined_hasher.hexdigest()

def modify_file(filepath, content_to_add="Modified content"):
    try:
        with open(filepath, 'a') as f:
            f.write(content_to_add)
    except FileNotFoundError:
        print(f"File not found: {filepath}")

def main(file_paths):
    original_top_hash = calculate_top_hash(file_paths)

    if original_top_hash is None:
        print("No valid files found for Top Hash calculation.")
        return

    print(f"Original Top Hash: {original_top_hash}")

    if file_paths:
        modify_file(file_paths[0])

    modified_top_hash = calculate_top_hash(file_paths)
    print(f"Modified Top Hash: {modified_top_hash}")

    if original_top_hash == modified_top_hash:
        print("Top Hash matches (modification failed/not detected).")
    else:
        print("Top Hash does not match (modification detected).")

if __name__ == "__main__":
    file_paths = ["L1.txt", "L2.txt", "L3.txt", "L4.txt"]
    for filepath in file_paths:
        with open(filepath, 'w') as f:
            f.write(f"Content of {filepath}")

    main(file_paths)

    for filepath in file_paths:
      try:
        os.remove(filepath)
      except FileNotFoundError:
        pass
