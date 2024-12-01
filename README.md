# Winter Supplement Rules Engine

[![Python Tests](https://github.com/Yurui-Feng/winter-supplement-rules-engine/actions/workflows/python-test.yml/badge.svg)](https://github.com/Yurui-Feng/winter-supplement-rules-engine/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Yurui-Feng/winter-supplement-rules-engine/branch/main/graph/badge.svg)](https://codecov.io/gh/Yurui-Feng/winter-supplement-rules-engine)

## Project Overview

A rules engine that determines client eligibility for the Winter Supplement and calculates the eligible supplement amount based on predefined rules. The engine integrates with a Winter Supplement Calculator web application through MQTT messaging.

## Features

- Determines eligibility for Winter Supplement based on `familyUnitInPayForDecember`
- Calculates supplement amounts based on:
  - Family composition (single/couple)
  - Number of dependent children
- Integrates with Winter Supplement Calculator via MQTT
- Real-time processing of eligibility requests

## Prerequisites

- Python 3.12 or higher
- Poetry (Python package manager)
- Internet connection (for MQTT broker access)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/winter-supplement-rule-engine.git
   cd winter-supplement-rule-engine
   ```

2. [Install poetry](https://python-poetry.org/docs/) 

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Running the Application

1. Activate the Poetry virtual environment:
   ```bash
   poetry shell
   ```

2. Run the rules engine with a specific MQTT topic ID:
   ```bash
   python main.py --topic-id TOPIC_ID
   ```

   Replace `TOPIC_ID` with the topic ID from the Winter Supplement Calculator web application.

## Running Tests

1. Ensure you're in the Poetry virtual environment:
   ```bash
   poetry shell
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run tests with coverage report:
   ```bash
   pytest --cov=rules_engine
   ```
