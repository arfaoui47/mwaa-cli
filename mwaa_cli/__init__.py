__version__ = "0.1.0"

import click
import base64
from typing import Tuple
import boto3
import requests
from dataclasses import dataclass
from mwaa_cli.config import AVAILABLE_CMDS


CLIENT = boto3.client('mwaa')


@dataclass
class CLIParameters:
    token: str
    host : str


def get_cli_parameters(environment_name: str) -> CLIParameters:
    cli_token = CLIENT.create_cli_token(Name=environment_name)
    return CLIParameters(token=cli_token['CliToken'], host=cli_token['WebServerHostname'])


def validate_cmd(command: str) -> bool:
    try:
        available_cmds = "\n   - ".join(AVAILABLE_CMDS)
        msg = f"Command: '{command}' not found. Available commands:\n   - {available_cmds}"
        assert command in AVAILABLE_CMDS, msg 
    except AssertionError as e:
        raise RuntimeError(e) 


def send_request(cli_parameters: CLIParameters, command: str) -> Tuple[str, str]:
    try:
        mwaa_response = requests.post(
            url=f"https://{cli_parameters.host}/aws_mwaa/cli",
            headers={
                'Authorization': f"Bearer {cli_parameters.token}",
                'Content-Type' : "text/plain",
            },
            data=command,
        )
        mwaa_std_err_message = base64.b64decode(mwaa_response.json()['stderr']).decode('utf8')
        mwaa_std_out_message = base64.b64decode(mwaa_response.json()['stdout']).decode('utf8')
    except Exception as e:
        mwaa_std_err_message = str(e)
        mwaa_std_out_message = ''

    return mwaa_std_out_message, mwaa_std_err_message


@click.command()
@click.option('--environment-name', '-e', prompt='Environment name', help='Environment name')
@click.option('--command', '-c', prompt='Command', help='Command')
def main(environment_name: str, command: str) -> None:
    validate_cmd(command)
    cli_parameters = get_cli_parameters(environment_name)
    std_out, std_err = send_request(cli_parameters, command)
    click.echo(std_out)
    click.echo(std_err)


if __name__ == '__main__':
    main()
