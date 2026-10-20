# NBA GameBoard Dashboard

## Dashboard
- Get context into upcoming NBA games including
    - NBA teams' over performance
    - previous games of the same matchup
    - NBA Reporter summary of other news (injury reports, etc.)

## Data Pipeline
```mermaid
    flowchart LR
    a(Data Source: NBA Stats API)
    b(Data Desitination: PostgreSQL database)

    subgraph Box ["Orchestration: GitHub Actions Cron Job"]
        a --Python_ETL_Script--> b
    end
```

## References
- NBA Stats API [Link](https://github.com/swar/nba_api)
    - An API client package to easily access the APIs of NBA.com
