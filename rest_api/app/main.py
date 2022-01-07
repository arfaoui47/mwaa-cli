from typing import Any, Optional
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Json
from mwaa_cli import send_request, get_cli_parameters


ENV = os.environ.get('ENV', 'dev')

class TiggerDAGConfig(BaseModel):
    dag_id: str
    config: Any
    run_id: Optional[str] = None


app = FastAPI()

# https://airflow.apache.org/docs/apache-airflow/2.0.2/cli-and-env-variables-ref.html#trigger
@app.post("/trigger_dag")
def run_cmd(dag_parms: TiggerDAGConfig):
    cli_parameters = get_cli_parameters(ENV)
    std_out, std_err = send_request(cli_parameters, dag_parms.json())
    return {'std_out': std_out, 'std_err': std_err}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
