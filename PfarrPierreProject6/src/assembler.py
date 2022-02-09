import argparse 
from whitespace import White_Space




















if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    # accept a postional arguement for the file path
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    args = parser.parse_args()

    file_in = args.file_path
    file_out = White_Space(file_in)
    file_out.clean()
 