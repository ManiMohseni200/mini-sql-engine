from loader import load_csv
from lexer import Lexer
from parser import Parser
from executor import Executor
from errors import SQLError

def main():
    table = load_csv("data/students.csv")

    lexer = Lexer()
    executor = Executor()

    print("mini SQL Engine")
    print("Type 'exit' to quit.")
    print()

    while True:

        try:
            query_text = input("sql> ")
            if query_text.strip().lower() == "exit":
                print("Goodbye!")
                break
            if not query_text.strip():
                continue

            tokens = lexer.tokenize(query_text)

            parser = Parser(tokens)

            query = parser.parse()

            result = executor.execute(
                query,
                table
            )

            result.print()

        except SQLError as error:
            print(f"SQL Error: {error}")

        except Exception as error:
            print(f"Unexpected Error: {error}")

if __name__ == "__main__":
    main()