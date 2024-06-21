from prefect_dbt.cli.commands import DbtCoreOperation
from prefect import flow
from pathlib import Path

@flow
def trigger_dbt_flow() -> str:
    dbt_dir = Path('/Users/thinhha/Documents/VGSales_DE_Project/dbt')
    result = DbtCoreOperation(
        commands=["dbt debug","dbt build -t dev --vars 'is_test_run: false'"],
        working_dir=dbt_dir,
        project_dir=dbt_dir,
        profiles_dir=dbt_dir
    ).run()
    return result

if __name__ == "__main__":
    trigger_dbt_flow()