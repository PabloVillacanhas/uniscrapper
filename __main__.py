from scrappers import usc


def main():
    array = usc.scrapper()
    for s in array:
        print(s)


if __name__ == "__main__":
    main()
