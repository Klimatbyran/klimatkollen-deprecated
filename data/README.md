# Climate Data Pipeline Overview

## General information

### Getting started

Run `pip install -r requirements.txt` to install the required dependencies. If you're using Python 3, you can replace `pip` with `pip3`.

### Example calculation

A Google Doc with example calculations for the emissions in Skövde municipality can be found [here](https://docs.google.com/document/d/1MihysUkfunbV0LjwSUCiGSqWQSo5U03K0RMbRsVBL7U/edit#heading=h.oqnz3ereclbn). The calculations for each step are described in words (in Swedish) and, where possible, an explicit and simple calculation is presented. NOTE: The calculations are done for 2024 year's budget and the document is intended as method desciption for non-coders and people that are new to the source code. The document is open and editable and may therefore be updated over time.

### Data Sources

We obtain our information from multiple providers including SMHI, SCB, Trafa, and PowerCircle. Some of this information is stored directly in our repository, while other datasets are dynamically pulled from their original locations.

### Data Transformation

We utilize Python libraries such as Pandas and NumPy to perform various calculations on the collected data. This allows us to tailor the data into a format that is easier to understand and display on our website.

### Repository Structure

- `/data:` This directory contains both the datasets we host and the Python scripts for calculations.
    - `climate_data_calculations.py`: Execute this Python script to run all the calculations and generate updated data.
- `/data/output:` This is where the processed data gets saved.
    - `climate-data.json`: This JSON file serves as the core output, containing all the calculated climate data.
- `/data/tests:` Unit tests for data calculations. To run all tests, stand in `/data/` and run

    ```
    python3 -m unittest discover -s tests
    ```

    To run a specific test file, stand in `/data/` and run

    ```
    python3 -m unittest tests/{filename}.py
    ```

    where you replace *filename* with the name of the actual test file.
    
    If you notice any test failing, please submit a ticket about it.

### Performance profiling

Requires Graphwiz installed on the OS https://www.graphviz.org/download/
```sh
py.test tests --profile-svg && open prof/combined.svg
```

### How to Update Data on Site

To recalculate and refresh the site's data, navigate to the `/data` folder and execute the following command:

`python3 climate_data_calculations.py`

The results will be saved in the `/data/output` folder, primarily in the `climate-data.json` file. The climate data is sourced using a TypeScript utility service located at `utils/climateDataService.tsx`. This service is responsible for fetching and manipulating the data found in `climate-data.json` for use throughout the website. To add or edit the descriptions of datasets that appear in the national overview on the website's homepage, make the necessary changes in `utils/datasetDefinitions.tsx`.

#### Handling Data Inconsistencies for Municipalities

Given that Klimatkollen focuses on data related to municipalities, it's often necessary to standardize the naming conventions for Swedish municipalities as they can vary across different datasets. The following are known cases:

- Falun: also called Falu kommun.
- Gotland: also called Region Gotland or Region Gotland (kommun).
- Upplands Väsby: alternate spelling includes Upplands-Väsby.
- Stockholm: also called Stockholms stad.
- Malmö: also called Malmö stad.

In the list, the term appearing before the colon (:) is the standardized name that we use in the repository. Any alternative names listed after "also known as" should be converted to this standard version when incorporating new data sets.

## Detailed explanations

### Emission Calculations 

The folder `/issues/emissions` contains files with functions to perform calculations related to CO2 emissions for municipalities, based on SMHI emission data and a given total CO2 budget for Sweden. Each function serves a specific purpose such as preprocessing data, calculating municipality-specific budgets, future trends or when the budget for a municipality will run out. Their order of execution is specified in `/issues/emissions/emission_data_calculations.py`.

#### Constants 

The most important constants in the module are `NATIONAL_BUDGET_15`, `NATIONAL_BUDGET_17`, `NATIONAL_OVERHEAD_17`, `BUDGET_YEAR`, `CEMENT_DEDUCTION`, `LAST_YEAR_WITH_SMHI_DATA` and `CURRENT_YEAR` as they determine the baseline and scope of the calculations.

* `NATIONAL_BUDGET_15`: Represents the total CO2 budget for a 50% chance of staying below 1.5 degrees, in metric tonnes.
* `NATIONAL_BUDGET_17`: Represents the total CO2 budget for a 50% chance of staying below 1.7 degrees, in metric tonnes.
* `NATIONAL_OVERHEAD_17`: Reprensents the total national overhead for `NATIONAL_BUDGET_17`, in metric tonnes.
* `BUDGET_YEAR`: Represents the year from which the CO2 budget applies.
* `CEMENT_DEDUCTION`: Represents the total CO2 emissions from cement production in municipalities with cement plants that were operational in 2015 or later.
* `LAST_YEAR_WITH_SMHI_DATA`: Represents the last year for which the [National Emission database](https://nationellaemissionsdatabasen.smhi.se/) has data.
* `CURRENT_YEAR`: Represents the year which is to be handled as current year.

#### Functions

Here's a summary of what the functions do, in order of execution in `/issues/emissions/emission_data_calculations.py`:

1. `get_n_prep_data_from_smhi`: Downloads data from SMHI and preprocess it into a pandas dataframe.

2. `deduct_cement`: Deducts cement emissions from specified municipalities.

3. `calculate_trend_coefficients`: Calculates linear trend coefficients for each municipailty based on SMHI data from 2015 onwards. This is done by fitting a straight line to the data using least square fit.

4. `calculate_approximated_historical`: Calculates approximated historical data values for years passed since the last year with SMHI data. This is done by interpolation using previously calculated linear trend coefficients.

5. `calculate_trend`: Calculates trend line for future years up to 2050. This is done by interpolation using previously calculated linear trend coefficients

6. `calculate_n_subtract_national_overheads`: Calculates the national overhead for a CO2 budget for `NATIONAL_BUDGET_15`, based on `NATIONAL_BUDGET_17` and `NATIONAL_OVERHEAD_17`. This is achieved by determining the proportion of the national overhead within the total budget and then calculating corresponding value for `NATIONAL_BUDGET_15`. All values are in metric tonnes.

7. `calculate_municipality_budgets`: Calculates municipality specific CO2 budgets by deriving budget shares from the SMHI data for each municipality (using grand fathering) and multiplying them with the given total CO2 budget.

8. `calculate_paris_path`: Calculates an exponential curve satisfying each municipality's CO2 budget (Paris Agreement path), starting from the year the budget kicks in.

9. `calculate_historical_change_percent`: Calculates the average historical yearly emission change in percent based on SMHI data from 2015 onwards.

10. `calculate_needed_change_percent`: Calculates the yearly decrease in percent needed to reach the Paris Agreement goal.

11. `calculate_hit_net_zero`: Calculates the date and year for when each municipality hits net zero emissions (if so). This, by deriving where the trend line crosses the time axis.

12. `calculate_budget_runs_out`: Calculates the year and date for when the CO2 budget runs out for each municipality (if so). This, by integrating the trend line over the time it takes for the budget to be consumed and see where we are at the time axis by that point.

13. `emission_calculations`: Orchestrates the execution of the above methods in sequence to perform all emission calculations for municipalities.




