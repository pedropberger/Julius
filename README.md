# Julius

projeto movido para o time mpes-uis

Robot that captures data from Transparency Portals and applies known metrics and typologies to investigate indicators of administrative impropriety (people holding two public positions - beyond what is allowed by law - contracts and purchases with inflated prices, etc.) or poor practices of transparency portals.

# About the Project

This project started as an initiative of the Innovation Unit servers of the Public Prosecutor's Office of the State of Espírito Santo, aiming to capture data to expand the possibilities of investigating administrative impropriety, evaluate the data made available by the portals (in compliance with Law 12.527/2011), and apply typologies that give indications of corrupt practices. The name "Julius" refers to and pays homage to the character Julius from the series "Everybody Hates Chris", as the first typology tested was the verification of people with two jobs (but in this case, undue accumulation of public positions), and also because of the second name of the first project collaborator, dev Fabrício Julio Correia de Almeida.

Because it is a learning tool and exclusively uses public government data, we chose to restart the project as an open initiative, starting its development in an unlinked manner from any institution and making the codes available here on Github. The idea is to test, improve, create and refine codes and functions with Data Engineering techniques, Artificial Intelligence, and good development practices based on what already works. That's why the Readme and all documentation (even the code comments) are in English as the standard language - learning English is always a good thing.

# How it works?

Julius works as an automation algorithm that captures data from Transparency Portals through their APIs.

Each transparency portal has APIs that allow extraction of the data it contains. These APIs refer to data of similar structure, according to the category of what is made available (remuneration, bids, contracts, etc.).

In theory, when all municipalities and government entities reach a "maximum level" of transparency, they will all have similar data being made available, varying according to the type of entity, for example: municipal councils usually do not have revenue and collection structures, public companies have different bidding processes, etc. Based on this principle, the number of APIs and data grows.

Not all data is structured. Contracts, bidding documents, minutes, and commitment notes are examples of unstructured data. Hence, complexity grows. What we hope in the medium term is this:

# FAQ Transparency Portals

A Transparency Portal is a website that aims to disseminate detailed data and information about the budget execution of Brazilian public agencies and third-sector entities that receive public funds. The tool also publishes data on transversal subjects or related to the function of most of these agencies.

A trend of Brazilian Transparency Portals is the availability of APIs to facilitate reading/extraction of data by automated means, this good practice (https://www.portaltransparencia.gov.br/api-de-dados) has been rapidly expanding both in portals created by public agencies and service providers. It is expected that each transparency portal will have at least one API to make all data required by the Access to Information Act available.

The data contained in portals is structured (salary tables, payments to third parties, transfers, financial revenues) and unstructured (contracts, bidding documents, commitment notes), varying according to the public sphere, type of autarky, and other elements.

# How it works

# Transparency portals

# Documentation

# How to collaborate

## Collaborators

| [<img src="https://github.com/pedropberger.png?size=115" width=115><br><sub>@pedropberger</sub>](https://github.com/pedropberger) | [<img src="https://github.com/mwildemberg.png?size=115" width=115><br><sub>@mwildemberg</sub>](https://github.com/mwildemberg) |
| :---: | :---: |
