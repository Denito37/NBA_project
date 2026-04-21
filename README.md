# NBA Team Performance Dashboard

## Dashboard Overview
Analyze NBA teams performance over the past decade (2015-2016 season -> 2025-2026 season) 

## Dashboard Features
- See how each player in a team contribute (Points, Assits, Rebounds) to the teams performance
- See a team's recent performance (last 10 games) compared to their average performance over the past year

## Data Architecture Overview
- Data Source: NBA Stats API
- Business Logic: Python ETL Script
- Data Destination: AWS RDS PostgreSQL database
- Scheduler: GitHub Actions cron job scheduler

## Data Source Reference 
- NBA Stats API [Link](https://github.com/swar/nba_api)
    - An API client package to easily access the APIs of NBA.com
