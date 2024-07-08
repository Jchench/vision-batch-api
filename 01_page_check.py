import os

def find_missing_files(directory, prefix, extension):
    files = sorted([f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)])
    numbers = [int(f[len(prefix):-len(extension)]) for f in files]
    missing_files = []
    
    for i in range(min(numbers), max(numbers)):
        if i not in numbers:
            missing_files.append(f"{prefix}{i}{extension}")
    
    return missing_files

# Example usage
directory = 'clean/PL103_325_results'
prefix = 'page_'
extension = '.txt'

missing_files = find_missing_files(directory, prefix, extension)
print(f"Missing files: {missing_files}")
