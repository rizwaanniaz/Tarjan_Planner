# TarjanPlanner: Route Optimization in Seoul

## Overview
TarjanPlanner is a Python-based project designed to calculate and optimize routes to visit multiple relatives in Seoul based on criteria such as cost, time, or a combination of both. The application integrates route visualization, data validation, and automated testing for enhanced functionality and reliability.

---

## Features
- Optimization Criteria: Choose between minimum cost, minimum time, or both.
- Data Validation: Ensures no duplicate or extra stops and verifies CSV data integrity.
- Graphical Visualization: Displays the route and transport modes on a map.
- Execution Time Logging: Tracks the runtime of the application.
- Automated Testing: Includes unit tests using `pytest` for core functionality.

---

## Installation, Usage, and Testing

1. **Install Python and Dependencies**:
   - Ensure Python 3.11+ is installed. Check using:
     ```bash
     python --version
     ```
   - Install required libraries using pip:
     ```bash
     pip install
     ```

2. **Setup Project Files**:
   - Clone the repository or download the project as a ZIP:
     ```bash
     git clone <URL>
     ```

3. **Run the Application**:
   - Execute the main script to launch the program:
     ```bash
     python main.py
     ```
   - Follow the prompts to select optimization criteria.
   - View the output:
     - Route summary with cost and time details.
     - Graphical visualization of the route.
   - Logs: Execution time and errors are displayed in the console during execution.
   in addition, genetic_algorithm run time and total program run times are logged to file journey_logs, together with date and time.

4. **Testing**:
   - Run the included unit tests using `pytest`:
     ```bash
     python -m pytest test_project.py
     ```
   - Features tested:
     - calculate_total_distance
     - compare_transport_modes
     - transport mode initialization
     - CSV file loading with error handling
     - load transport modes
     - test Segment initialization

---

## Troubleshooting

**Common Issues and Solutions**:

1. **Python Version Issue**:
   - **Problem**: The program doesn’t run or modules are unavailable.
   - **Solution**: Install Python 3.11+ from [python.org](https://www.python.org/downloads/).

2. **Missing Dependencies**:
   - **Problem**: ModuleNotFoundError for libraries like `matplotlib` or `pytest`.
   - **Solution**: Install dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

3. **CSV File Errors**:
   - **Problem**: FileNotFoundError or incorrect data is loaded.
   - **Solution**: Ensure `locations.csv` and `transport_modes.csv` exist in the correct format.

4. **Pytest Not Running**:
   - **Problem**: Tests fail or pytest is not found.
   - **Solution**: Run tests using:
     ```bash
     python -m pytest test_project.py
     ```

---
