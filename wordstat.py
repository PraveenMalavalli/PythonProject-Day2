import argparse

from word_counter import count_word


def main():
    parser  = argparse.ArgumentParser(
        description="Reading the file"

    )

    parser.add_argument("-r", 
                        "--read", 
                        type=str, 
                        required=True,
                        metavar="FILE",
                        dest="file_name_path",
                        help="File path for .txt file"
                        )

    parser.add_argument("-t", 
                        "--top", 
                        type=int, 
                        metavar="N",
                        default=10,
                        help="Number of top words to display"
                        )

    args = parser.parse_args()

    if args.top <= 0:
        parser.error(f"Please enter the valid number for displaying, current number: {args.top}")

    try:
        with open(args.file_name_path, "r") as file:
            content = file.read()
        print(content)

    except FileNotFoundError:
        parser.error(f"File not found with name: {args.file_name_path}")

    except (OSError, UnicodeError) as error:
        parser.error(f"Unable to read file: {error}")


    top_words = count_word(content, args.top)


    for index, (word, count) in enumerate(top_words, start=1):

        print(f"{index}) {word} : {count}")

