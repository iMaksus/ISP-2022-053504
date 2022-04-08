from serializer import JsonSerializer

def main():
	js = JsonSerializer("Hello world!")
	js.printstr()

if __name__ == "__main__":
	main()

test_dict = {
	1: "Hello",
	2: "World",
	3: "!"
}