# finance-gpt

Finance GPT is a generative AI chatbot built on [Streamlit](https://streamlit.io/) that effectively addresses user queries by utilizing a vector-based document database. It allows users to get answers to queries related to any financial documents such as annual reports of listed companies or CSV/Excel of their financial figures. By employing the Retrieval-Augmented Generation (RAG) framework, uploaded document serve as context for generating responses through a large language model (LLM) using [LangChain](https://www.langchain.com/).

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Customizations](#customizations)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)


## Setup Instructions

After cloning the repository, follow these steps to set up the project:

1. **Set Up your development environment**:
   - Download and install JetBrains PyCharm IDE or your preferred IDE.
   - The following instructions will focus on PyCharm, but most IDEs provide similar features.

2. **Open the project**:
   - In PyCharm, navigate to `File -> Open` and select the cloned repository folder.

3. **Set Up a local virtual environment**:
   - Go to `Settings` > `Project: finance-gpt` > `Python Interpreter` > `Add Interpreter`.
   - Choose `Add Local Interpreter` > `Virtualenv Environment`.
     1. Select `Environment` -> `New`.
     2. Set `Base Interpreter` to your installed Python version (e.g., Python 3.x).
     3. Click `OK`.

4. **Install dependencies**:
   - Run the following commands in your terminal:
     ```bash
     pip install "generative-ai-hub-sdk[all]==1.2.2" --extra-index-url https://int.repositories.cloud.sap/artifactory/api/pypi/proxy-deploy-releases-hyperspace-pypi/simple/
     pip install -r requirements.txt
     ```
   - If you prefer to connect directly to the LLM via OpenAI instead of using the SAP proxy, you can skip the installation of `generative-ai-hub-sdk` and install required LangChain libraries instead.

5. **Run the application**:
   ```bash
   streamlit run finance-gpt.py
   ```
   
6. **Access the user interface**:
Open your web browser and navigate to [http://localhost:8500/](http://localhost:8500/) (or the appropriate port if different).

## Usage
Once the application is running, you can interact with finance-gpt by uploading your file and entering your in the selected interface. The chatbot will retrieve relevant information from the document and generate responses based on the context.

## Screenshots
Here are some screenshots showcasing working deployments of the application.
- Chat inteerface selection:
<img width="679" alt="1-interaction-types" src="https://github.com/user-attachments/assets/6f463af0-ad00-4584-a31c-105a359f574f">


- _PDF_ interaction type:
<img width="1713" alt="2-pdf-1" src="https://github.com/user-attachments/assets/9a274f53-8780-4290-bc36-ff7016930157">

<img width="1727" alt="3-pdf-2" src="https://github.com/user-attachments/assets/da7670dd-82f4-4558-b39a-8e5f4546d3c0">


- _EXCEL_ interaction type:
<img width="1727" alt="4-csv-line" src="https://github.com/user-attachments/assets/7948e12f-eaac-4f03-85c3-7e7b3b36fea9">

<img width="1171" alt="5-csv-bar" src="https://github.com/user-attachments/assets/5d351761-fc3b-4e59-9a97-66c8f10f01af">


## Customizations
You can easily customize the application in the following ways:
- Financial documents are just a use case for the RAG, same application can be generalised to query any kind of PDFs and CSVs.
- Modify the `properties.yml` file to adjust various flags and properties (e.g., enabling calls to the LLM without context if call with context does not give relevant response) to suit your requirements.

## Deployment
Here are a few options for deploying the application:
- [Streamlit Community Cloud](https://share.streamlit.io/deploy)
- Cloud Foundry: Relevant files for deployment through SAP BTP are included in the repository.


## Contributing
We welcome contributions to enhance finance-gpt! Please fork the repository and submit a pull request for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
