import zipfile
import os
import sys

# Try to import bzip2 and lzma. They are standard but optional.
try:
    import bz2
except ImportError:
    bz2 = None
    
try:
    import lzma
except ImportError:
    lzma = None

def get_available_methods():
    """Returns a list of supported compression method names."""
    methods = ['store', 'deflate']
    if bz2:
        methods.append('bzip2')
    if lzma:
        methods.append('lzma')
    return methods

def compress(source_path, manz_path, compression_level=9, method='deflate'):
    """
    Compresses a source file or directory into a .manz file.
    
    :param source_path: Path to the source file or directory.
    :param manz_path: Path to the output .manz file.
    :param compression_level: 1 (fastest, low) to 9 (slowest, max).
    :param method: 'store', 'deflate', 'bzip2', or 'lzma'.
    """
    
    # --- Map method name to zipfile constant ---
    method_map = {'store': zipfile.ZIP_STORED, 'deflate': zipfile.ZIP_DEFLATED}
    if bz2:
        method_map['bzip2'] = zipfile.ZIP_BZIP2
    if lzma:
        method_map['lzma'] = zipfile.ZIP_LZMA

    if method not in method_map:
        print(f"Error: Method '{method}' not available. Falling back to 'deflate'.", file=sys.stderr)
        method = 'deflate'
        
    zip_method = method_map[method]
    
    # Clamp compression level
    level = max(1, min(compression_level, 9))
    
    try:
        with zipfile.ZipFile(
            manz_path, 'w', 
            compression=zip_method, 
            compresslevel=level if method != 'store' else None
        ) as zf:
            
            if os.path.isdir(source_path):
                print(f"Compressing directory: {source_path} (Method: {method})")
                
                # Get the parent directory to make paths relative
                parent_dir = os.path.dirname(source_path)
                
                for root, dirs, files in os.walk(source_path):
                    # Add the directory entry itself
                    dir_name = os.path.relpath(root, parent_dir)
                    zf.write(root, arcname=dir_name)
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Archive name is relative path inside the zip
                        archive_name = os.path.relpath(file_path, parent_dir)
                        print(f"  ...adding {archive_name}")
                        zf.write(file_path, arcname=archive_name)
                        
            elif os.path.isfile(source_path):
                print(f"Compressing file: {source_path} (Method: {method})")
                archive_name = os.path.basename(source_path)
                zf.write(source_path, arcname=archive_name)
                
            else:
                print(f"Error: Path '{source_path}' is not a valid file or directory.", file=sys.stderr)
                return False
                
        print(f"Successfully compressed to '{manz_path}'")
        return True

    except FileNotFoundError:
        print(f"Error: Source path '{source_path}' not found.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An error occurred during compression: {e}", file=sys.stderr)
        return False

def decompress(manz_path, output_directory):
    """
    Decompresses a .manz file into a specified directory.
    
    :param manz_path: Path to the .manz file.
    :param output_directory: Folder where files will be extracted.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        with zipfile.ZipFile(manz_path, 'r') as zf:
            print(f"Decompressing '{manz_path}' to '{output_directory}'")
            zf.extractall(path=output_directory)
            print("Decompression successful.")
            return True
            
    except zipfile.BadZipFile:
        print(f"Error: '{manz_path}' is not a valid .manz (zip) file.", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: File '{manz_path}' not found.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An error occurred during decompression: {e}", file=sys.stderr)
        return False

def list_contents(manz_path):
    """
    Lists the contents of a .manz file without extracting.
    
    :param manz_path: Path to the .manz file.
    :return: A list of file names, or None if an error occurred.
    """
    try:
        with zipfile.ZipFile(manz_path, 'r') as zf:
            return zf.namelist()
            
    except zipfile.BadZipFile:
        print(f"Error: '{manz_path}' is not a valid .manz (zip) file.", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: File '{manz_path}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An error occurred while listing contents: {e}", file=sys.stderr)
        return None