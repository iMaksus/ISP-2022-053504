from my_serializer.converter import Converter

def main():
    converter = Converter()
    converter.get_args()
    converter.parse_args()


if __name__ == "__main__":
    main()
