import argparse
import manz_compressor # Imports the file we just updated

def main():
    print("--- Manz Compressor CLI ---")
    print("--- Made by Manz @manz.shh ---\n")
    
    parser = argparse.ArgumentParser(description="Manz Compressor CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Compress Command ---
    comp_parser = subparsers.add_parser("compress", help="Compress a file or directory.")
    comp_parser.add_argument("source", type=str, help="The source file or directory to compress.")
    comp_parser.add_argument("destination", type=str, help="The output .manz file path.")
    comp_parser.add_argument(
        "-l", "--level", 
        type=int, 
        default=9, 
        choices=range(1, 10), 
        help="Compression level (1=fast, 9=max). Default is 9."
    )
    comp_parser.add_argument(
        "-m", "--method", 
        type=str, 
        default="deflate", 
        choices=manz_compressor.get_available_methods(), 
        help="Compression method (e.g., deflate, lzma, bzip2)."
    )

    # --- Decompress Command ---
    decomp_parser = subparsers.add_parser("decompress", help="Decompress a .manz file.")
    decomp_parser.add_argument("source", type=str, help="The .manz file to decompress.")
    decomp_parser.add_argument("destination", type=str, help="The output directory.")

    # --- List Command (NEW) ---
    list_parser = subparsers.add_parser("list", help="List contents of a .manz file.")
    list_parser.add_argument("source", type=str, help="The .manz file to inspect.")

    # --- Parse Arguments and Run ---
    args = parser.parse_args()

    if args.command == "compress":
        manz_compressor.compress(args.source, args.destination, args.level, args.method)
    elif args.command == "decompress":
        manz_compressor.decompress(args.source, args.destination)
    elif args.command == "list":
        print(f"Listing contents of '{args.source}':")
        contents = manz_compressor.list_contents(args.source)
        if contents:
            for item in contents:
                print(f"  - {item}")
        else:
            print("Could not list contents.")

if __name__ == "__main__":
    main()