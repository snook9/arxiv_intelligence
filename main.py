from services.api.arxiv_api import ArxivApi

if __name__ == '__main__':

    print("Hello World!")
    data = ArxivApi().getData()
    print(data.read().decode('utf-8'))
