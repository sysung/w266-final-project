# Identifying Misinformation in Social Media and New Sources

This is the repo for the W266 Final Project which holds the code, model, papers, and other resources for misinformation detection.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Downloading the Dataset](#downloading-the-dataset) 
- [Usage](#usage)
- [Contributing](#contributing)

## Project Overview

Misinformation on social media platforms has been running rampant in the past few years with false claims. It is imperative that people obtain news from reliable unbiased sources to help people make informed decisions.

To ensure that misinformation does not become widespread, we are proposing an NLP model to detect and classify fake news. Our model will utilize transformers to identify misinformation by analyzing the context of the articles.

### Importance and Challenges of Misinformation

Misinformation carries many consequences including confusion, fear, and panic that can be harmful to individuals and society. For example, misinformation about the COVID-19 vaccine being dangerous caused people to not take the drug which resulted in many preventable deaths.

However, identifying misinformation can be challenging because it is often disguised within legitimate information which can propagate through different mediums like social media and new outlets. Additionally, people are more likely to believe in misinformation that aligns with their pre-existing beliefs and biases. Therefore, it is often difficult for humans to catch fake news before it spreads.

There are many types of misinformation such as click bait, political bias, and government propaganda that will require extensive research and data collection that may stretch beyond the scopes of the course. Therefore, we will be timeboxing specifically focusing on fake news by analyzing a dataset in the paper WatClaimCheck that provides evidence refuting or supporting a claim


## Features

List the key features of your project. This can be in the form of a bulleted list or a table. 

- Feature 1
- Feature 2
- Feature 3

## Getting Started

Explain how to get started with your project. Provide step-by-step instructions, including code examples if necessary.

### Prerequisites

List any software, libraries, or dependencies that users need to have installed before they can use your project.

### Installation

#### Downloading the Dataset

To download the dataset, go to the [WatClaimCheck Git Repo](https://github.com/nxii/WatClaimCheck/tree/main) and submit a [Google Forms](https://forms.gle/sEZjvJqmyHdR4AMKA) to receive a copy of the dataset.

#### Creating Conda Environment

Create the conda environment using the ./env file

`conda env create --prefix ./envs -f environment.yml`

Once the environment has been created, you can activate it using the following command

`conda activate ./envs`

To shorten the long prefix in the shell, use the following command. You'll need to deactivate and reactivate for the change to take effect

`conda config --set env_prompt '({name})'`

If you have a library to add, you can use the following command to add it into the environment.yml so that the libraries are shared

`conda env export -f environment.yml`

For more information about conda, see https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments

## Usage

## Reference Links
- [WatClaimCheck Git Repo](https://github.com/nxii/WatClaimCheck/tree/main)