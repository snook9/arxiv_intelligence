from services.api.arxiv_api import ArxivApi

if __name__ == '__main__':

    print("Hello World!")
    pdf_list = ArxivApi().get_pdf()
    for pdf in pdf_list:
        print("PDF:", pdf)
