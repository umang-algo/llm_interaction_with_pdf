# Umang's PaperPal: Your Trusted Companion for PDF Queries

Umang's PaperPal is a Streamlit application designed to help you interact with PDF documents using OpenAI's GPT-3.5 Turbo model. The app allows you to upload a PDF, view its pages with enhanced quality, and ask questions about its content. Your interactions are saved to a local SQLite database for future reference.

![image](https://github.com/user-attachments/assets/cf7198d5-44e6-4c40-abb7-59f34a6e8d75)




## Features

- **User Authentication**: Simple login system to secure access.
- **PDF Upload and Viewing**: Upload a PDF file and view its pages with improved image quality.
- **Question-Answering System**: Ask questions about the content of the uploaded PDF and get responses from GPT-3.5 Turbo.
- **Interaction Logging**: Save questions and answers to a local SQLite database with timestamps.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- OpenAI API Key
- Additional Python libraries (specified in `requirements.txt`)

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-username/umangs-paperpal.git
    cd llm_interaction_with_pdf
    ```

2. **Create a virtual environment and activate it**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required libraries**

    ```bash
    pip install -r requirement.txt
    ```

4. **Run the application**

    ```bash
    streamlit run llm_to_chat_with_pdf
    ```

## Usage

1. **Login**

    Enter your username and password to access the application.

2. **Enter OpenAI API Key**

    Provide your OpenAI API key to enable the question-answering functionality.

3. **Upload a PDF**

    Use the file uploader to select and upload a PDF document.

4. **View PDF Pages**

    The uploaded PDF pages will be displayed with enhanced quality in the left column.

5. **Ask Questions**

    Type your questions about the PDF content in the text area on the right and click "Submit" to get responses from the AI. Your interactions will be saved to the local SQLite database.

## Database

The interactions are stored in a SQLite database (`chat_data.db`) with the following schema:

- `id` (INTEGER, PRIMARY KEY)
- `username` (TEXT)
- `question` (TEXT)
- `answer` (TEXT)
- `timestamp` (TEXT)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenAI](https://www.openai.com/)
- [LangChain](https://www.langchain.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)



