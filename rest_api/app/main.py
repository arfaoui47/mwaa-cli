from typing import Any, Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Json


class TiggerDAGConfig(BaseModel):
    dag_id: str
    config: Any
    run_id: Optional[str] = None


app = FastAPI()

# https://airflow.apache.org/docs/apache-airflow/2.0.2/cli-and-env-variables-ref.html#trigger
@app.post("/trigger_dag")
def run_cmd(dag_parms: TiggerDAGConfig):
    print(dag_parms)
    return {'dag_id': dag_parms.dag_id, 'run_id': dag_parms.run_id}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
