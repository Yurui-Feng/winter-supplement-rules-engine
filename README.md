  # Winter Supplement Rules Engine

  ## Project Overview

  A rules engine to determine client eligibility for the Winter Supplement and calculate the eligible supplement amount based on predefined rules.

  ## Prerequisites


  ## Installation Instructions

  1. Clone the repository:

     ```bash
     git clone https://github.com/yourusername/winter-supplement-rule-engine.git
     cd winter-supplement-rule-engine
     ```

  2. Install dependencies:

     ```bash
     poetry install
     ```

  ## MQTT Topic ID Guidance

  - Obtain the MQTT topic ID from the Winter Supplement Calculator web application.
  - Update the `topic_id` variable in `main.py` or pass it as a command-line argument:

    ```bash
    python main.py --topic-id YOUR_TOPIC_ID
    ```

  ## Running the Application
