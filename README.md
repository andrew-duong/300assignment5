# Olympic Archery Database Application

## Overview
This Python application interfaces with the Olympic Archery Database, which contains summarized results of archery events at the Tokyo 2020 Olympic Games. The data is adapted from the official results provided by the IOC.

For more information about the Tokyo 2020 Olympics, visit [official website](https://olympics.com/en/olympic-games/tokyo-2020).

## Database Description
The database includes information on registered participants, events, medals, and more. Here's a brief overview:

- Registered participants: Athletes and coaches are assigned Olympic ID numbers. Athletes provide details like year of birth, sex, and their first games.
- Events: Five archery events scheduled across five different days.
- Medals: Participants can earn bronze, silver, or gold medals.
- Country Medals: A table summarizes the total archery medals won by each country since 1972.

## Usage
### Task 1: Python Application
Developed Python application features:

1. User authentication: Requires login credentials to connect to the database.
2. Operation selection: Choose between insert, delete, update, create table, create view, alter, and query.
3. User-friendly prompts: Gather information step by step, ensuring valid SQL command creation.
4. SQL execution: Construct SQL commands, execute them using MySQL connector, and display results.
5. Endless loop: Application runs until the user chooses to quit.

### Task 2: Relational Algebra Queries
Includes a set of queries written in relational algebra expressions.

## Database Setup
1. Execute the provided `olympicarchery.sql` file in MySQL Workbench to create and populate the schema.

## How to Run
1. Clone this repository.
2. Make sure you have Python installed.
3. Install the required libraries, e.g., MySQL connector.
4. Run the Python application to interface with the database.

## Report
The repository includes a report with the following details:
- Group information and repository link.
- Task distribution (who implemented what, reviewed, and tested what).
- Screenshots of continuous integration testing.
- Screenshots comparing application output with MySQL client/workbench queries.
- Database access information (if applicable).

## Disclaimer
- Ensure the database is included in the repo.
- Do not hardcode connection information.
- Follow good git hygiene practices.

## Queries (Ungraded)
A set of queries is provided as part of Task 2 for your own knowledge.

---

This project was adapted from the ENSF 300 Fall 2022 course.