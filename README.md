# Julius

Tool that captures data from Transparency Portals and applies known metrics and typologies to investigate indicators of administrative impropriety (people holding two public positions - beyond what is allowed by law - contracts and purchases with inflated prices, etc.) or poor practices of transparency portals.

# About the Project

This project started as an initiative of the Innovation Unit servers of the Public Prosecutor's Office of the State of Espírito Santo to apply data science and automation techniques, back in 2018. The idea was to extract data from portals to expand the possibilities of investigating administrative impropriety, evaluate the data made available by the portals (in compliance with Law 12.527/2011), and apply typologies that give indications of corrupt practices.

The name "Julius" refers to and pays homage to the character Julius from the series "Everybody Hates Chris", as the first typology tested was the verification of people with two jobs (but in this case, undue accumulation of public positions), and also coincidentally because it's the middle name of the first project collaborator, dev Fabrício Julius Correia de Almeida.

Because it is a useful learning tool and exclusively uses public government data, in 2023 we chose to restart the project as an open initiative, with development and sharing unlinked from bureaucracies and making the codes available here on Github. The idea is, based on what already works, to test, improve, create and refine codes and functions with Data Engineering techniques, Artificial Intelligence and good development practices.

The codes are simple and the tools are the most basic available for data engineering, making it easy to replicate and creating a learning environment for anyone who wants to learn, whether they are public servants, university students, online course students, or just enthusiasts.

# How it works?

Julius works as an automation algorithm that captures data from Transparency Portals through their APIs.

Each transparency portal has APIs that allow extraction of the data it contains. These APIs refer to data of similar structure, according to the category of what is made available (remuneration, bids, contracts, etc.).

In theory, when all municipalities and government entities reach a "maximum level" of transparency, they will all have similar data being made available, varying according to the type of entity. For example: Municipal councils usually do not have revenue and collection structures, public companies have different bidding processes, etc. Based on this principle, the number of APIs and data grows.

Not all data is structured. Contracts, bidding documents, minutes, and commitment notes are examples of unstructured data. This is where complexity grows. This is the challenge. But working on this adds value to data and tools. Unstructured data can be stored in NoSQL databases, their texts can be extracted for use and feeding NLP applications, for example.

Julius consumes the APIs of all implemented transparency portals (so far, the 78 municipalities of the state of Espírito Santo) and stores them in a database. This database is available for use within the docker container. From there you can download, share, consume in your applications or use as you see fit.

![image](https://user-images.githubusercontent.com/98188778/235966779-ca954c0f-3407-4c7c-b548-2feb677fe1fc.png)

# Expected Results

They say that data is the oil of the present, right?

Supervisory bodies (Public Prosecutor's Offices, Courts of Auditors, CGU, etc.) and the municipalities and councils themselves have worked hard in the last decade to put into practice and meet the requirements of the Access to Information Law, optimizing transparency portals to guarantee people access to reliable and quality data, and enable this access including through automated means (APIs, webservices, etc.).

In other words, we have thousands of wells of this future oil waiting to be extracted, processed, refined, observed and used for the benefit of society.

Julius is code that only seeks to take the first step. Which is to extract, organize and store this product efficiently.

The tool is open source, all the data and application stack used here will be Open Source, and the data extracted by it is also public, a right guaranteed in the Constitution to all Brazilians.

After Julius, the use of the data is free. But we leave as suggestions good practices: create tools for automated supervision and analysis of expenses, textual analysis of contracts to identify fraud, creation of a price consultation system, identification of cartel practices and personal learning.

# How to Use?

Simply install docker (https://www.docker.com) in your environment.

Download the Dockerfile present at the root of the github directory.

Place the file in the directory you like best.

Activate your command line shell (Bash, PowerShell, CMD) in the directory where the dockerfile is located.

Execute the following command to create a shared volume, where you can later save/exchange files with the application:

```bash
docker volume create dados
```

Create the container image from the dockerfile:

```bash
docker build -t julius-img .
```

And finally, put the container into operation:

```bash
docker run -d --name julius julius-img
```

Done!

The created container will download the necessary codes and start executing the application. In your storage you will be able to find the SQLite database. Now just wait a few hours and the data will be saved in the database.

The commands above are not a rule, you can customize the volume, image and container using other docker commands you find interesting.

# The Challenge

There is no universal standard or rule for the operation or format of transparency portals. The same goes for their consumption APIs. In other words, even though every portal must make available the data required by the Access to Information Law, it can make it available in the way it wants, or is most practical for it.

For example: Municipality X's API returns data related to payroll in a JSON file and municipality Y returns it in a *.csv table, or, municipality Z brings after the CNPJ the bidding process number that originated the contract in its contracts section, while council Z only brings the CNPJ.

None of the above cases violates the Access to Information Law, since the data is made available. However, it requires data engineering if you want to make a comparison or insert all data into the same base. This is the puzzle we want to solve.

The good news? by luck or chance, few companies/formats are applied to several portals. In the state of Espírito Santo, for example, we have 3 portal models for 78 municipalities. So just write the code to pull the API data from one municipality, and you can replicate it to a dozen of them.

*We want to complete Brazil. We already have 78 municipalities, only 5,490 to go! Shall we work together on this?*

# Computational Challenges

Are you a dev? Help us solve these problems.

- **Multithreading**: It takes several hours to complete the data extraction. This is because we limit the data from 2020 onwards. Multithreading, parallel processes and other forms of parallel code execution would apparently be the solution. But when we tried to implement it, we had the IP blocked obviously due to many requests from the same source.

- **Code Organization**: We are still learning to write beautiful and readable codes. Any implementation (or tip) that improves the aesthetics and readability of the code is welcome. Even organizing folders efficiently was difficult to decide.

- **Collaboration**: Merge, branch, pull, all of this is new to us. We need good souls to guide us on how to do this better to evolve the tool.

- **Modularization**: The project starts with 78 portals of 4 different formats. How can we optimize the code so that people can add more portals and formats and include this in the application without messing up the operation? We have a plan, but I know there are people much more prepared and experienced for this.

- **Unstructured Data**: Some portals bring files in pdf, word and text to make contracts, bidding documents, commitment notes, etc. available in full. This is a world to be explored. Whether applying an OCR algorithm to extract text from pdfs or thinking and deciding the best way to store and work with this data.

# Project Structure

The project is organized into the following directories:

- `modules/`: Contains the specific modules for each data provider (company).
  - `{company}/`: Each company has its own module with its own data and methods.
    - `__init__.py`: Makes the directory a Python module.
    - `agents.md`: Specific documentation for the data collection of the company.
    - `api_metodos/`: API methods and other relevant information.
    - `prefeituras.csv`: List of municipalities that use the company's platform.
    - `tests/`: Directory for specific tests for this module.
- `data/`: Contains the extracted data in Parquet format.
  - `parquet/`: Root directory for the Parquet files.
    - `{municipality}/`: Each municipality has its own directory.
      - `{year}/`: Each year has its own directory.
        - `{endpoint}.parquet`: File with the data from the endpoint.
- `main.py`: Main script of the project.
- `README.md`: This file.

# How to Run

To run the data extraction, you need to have Python 3 and the required packages installed.

## Installing dependencies

```bash
pip install -r requirements.txt
```

## Running the application

To run the data extraction for the `portaltp` module, simply run the `main.py` script:

```bash
python3 main.py
```

## Configuring the execution

You can configure the years and months to be extracted by editing the `modules/portaltp/config.py` file.

## Resulting data

The extracted data will be saved in the `data/portaltp/` directory in Parquet format. Each municipality and endpoint will have its own file.

A control file named `control_portaltp.json` will also be created in the `data/` directory to keep track of the executed tasks.

# Transparency Portals

A Transparency Portal is a website that aims to disseminate detailed data and information about the budget execution of Brazilian public agencies and third-sector entities that receive public funds. The tool also publishes data on transversal subjects or related to the function of most of these agencies.

A trend of Brazilian Transparency Portals is the availability of APIs to facilitate reading/extraction of data by automated means. This good practice (https://www.portaltransparencia.gov.br/api-de-dados) has been rapidly expanding both in portals created by public agencies and service providers. It is expected that each transparency portal will have at least one API to make all data required by the Access to Information Law available.

The data contained in portals is structured (salary tables, payments to third parties, transfers, financial revenues) and unstructured (contracts, bidding documents, commitment notes), varying according to the public sphere, type of agency, and other elements.

The items below are commonly found in transparency portals, and each of them represents a specific section with information about a certain subject related to the activities of a government entity:

- **Bids (Licitações)**: administrative processes that aim to select the best proposal for contracting services, works or supply of goods. Information about bids generally includes dates, modalities, values, participating and winning companies.

- **Contracts (Contratos)**: formal agreements signed between a government entity and a third party, whether an individual or legal entity, for the provision of services, works or supply of goods. Information about contracts generally includes values, contract object, deadlines and conditions.

- **Minutes (Atas)**: documents that record the main facts and decisions of a meeting or public session. Information about minutes generally includes dates, times, agenda and resolutions.

- **Purchase Orders (Ordem de compras)**: documents issued for the acquisition of materials or services. Information about purchase orders generally includes dates, values, suppliers and description of acquired items.

- **Material Entries (Materiais entradas)**: records of materials received by the government entity, whether through purchases, donations or other forms of acquisition. Information about material entries generally includes dates, values, suppliers and description of items.

- **Material Exits (Materiais saídas)**: records of materials that left the government entity, whether through transfers, disposals or other forms of write-off. Information about material exits generally includes dates, values and destination of items.

- **Consolidated Assets (Bens consolidado)**: a record of the government entity's patrimonial assets, both movable and immovable. Information about consolidated assets generally includes description, value, location and status of assets.

- **Movable Assets (Bens móveis)**: records of the government entity's patrimonial assets that can be moved, such as vehicles, equipment and furniture. Information about movable assets generally includes description, value, serial number and acquisition date.

- **Immovable Assets (Bens imóveis)**: records of the government entity's patrimonial assets that cannot be moved, such as land and buildings. Information about immovable assets generally includes description, value, location and built area.

- **Vehicle Fleet (Frota de veículos)**: a record of vehicles used by the government entity, whether for transporting people, goods or public services. Information about vehicle fleet generally includes model, license plate, year of manufacture and mileage.

- **Revenue Budget (Orçamento de receitas)**: a record of the government entity's revenue forecasts for a certain period. Information about revenue budget generally includes collection sources, values and validity period.

- **Revenue Execution (Execução de receitas)**: a record of revenues actually collected by the government entity in a certain period. Information about revenue execution generally includes collection sources, values and reference period.

- **Expense Budget (Orçamento de Despesas)**: the forecast of expenses that a public body will have during a certain period. In the transparency portal, this information is detailed by expense category, program and budget unit, enabling citizens to have a broad view of the resources that will be used and for what purposes.

- **Commitments (Empenhos)**: the record of a spending commitment assumed by the public body, which will be paid later. This information is important so that citizens can track expenses made by the body and verify if they are within the planned budget.

- **Liquidations (Liquidações)**: the confirmation that a planned expense was actually carried out by the public body. This information is important so that citizens can verify if the public resource was used as planned and if the execution of the expense was adequate.

- **Payments (Pagamentos)**: the record of the actual payment of an expense made by the public body. This information is important so that citizens can track if expenses were paid within the established deadline and if the amount actually paid corresponds to the planned amount.

- **Extra-budgetary Transfers (Transferências Extraorçamentárias)**: transfers of financial resources between government entities that are not provided for in the annual budget. This information is important so that citizens can verify if these transfers are being carried out adequately and transparently.

- **Intra-budgetary Transfers (Transferências Intraorçamentárias)**: transfers of financial resources between budget units within the same government body. This information is important so that citizens can track how resources are being distributed within the body and if they are being used efficiently.

- **Public Servants (Servidores)**: information about public employees who work in the government body. In the transparency portal, it is possible to find data on the organizational structure of the body, the number of employees by position and their salaries, among other information. This information is important so that citizens can evaluate the efficiency and quality of services provided by the body.

# Collaborators

| [<img src="https://github.com/pedropberger.png?size=115" width=115>](https://github.com/pedropberger) <br> [@pedropberger](https://github.com/pedropberger) | [<img src="https://github.com/mwildemberg.png?size=115" width=115>](https://github.com/mwildemberg) <br> [@mwildemberg](https://github.com/mwildemberg) | [<img src="https://github.com/iaraarruda.png?size=115" width=115>](https://github.com/iaraarruda) <br> [@iaraarruda](https://github.com/iaraarruda) | [<img src="https://github.com/gMerisio.png?size=115" width=115>](https://github.com/gMerisio) <br> [@gMerisio](https://github.com/gMerisio) | [<img src="https://github.com/HeitorQuartezani.png?size=115" width=115>](https://github.com/HeitorQuartezani) <br> [@HeitorQuartezani](https://github.com/HeitorQuartezani) |
|:---:|:---:|:---:|:---:|:---:|

Help us evolve and join the group.
