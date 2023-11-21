import os
import logging
import subprocess
from halo import Halo


def create_spark_hadoop_network():
    network_name = 'spark-hadoop-network'
    spinner = Halo(text=f'Checking for existing network: {network_name}')

    spinner.start()
    existing_networks = subprocess.run(['docker', 'network', 'ls'], capture_output=True, text=True)
    if network_name in existing_networks.stdout:
        spinner.succeed(f'Network {network_name} already exists')
        return True

    spinner.text = f'Creating shared network: {network_name}'
    try:
        subprocess.run(['docker', 'network', 'create', network_name], check=True)
        spinner.succeed(f'Network {network_name} created')
    except subprocess.CalledProcessError as e:
        spinner.fail(f'Error creating network: {e}')
        logging.error(f'Error during network creation: {e}')
        return False
    return True


def start_container(container_dir):
    command = ['docker', 'compose', 'up', '-d']
    spinner = Halo(text=f'Starting containers in {container_dir}', spinner='dots')
    spinner.start()
    os.chdir(container_dir)
    try:
        subprocess.run(command, check=True)
        os.chdir('..')
        spinner.succeed('Containers started')
    except Exception as e:
        spinner.fail(f'Error starting Docker containers: {e}')
        logging.error(f'Error during data processing: {e}')
        return False
    return True


def setup_environment():
    hadoop_container_dir = 'hadoop-spark'

    if create_spark_hadoop_network() and start_container(hadoop_container_dir):
        print("Environment setup completed successfully.")
    else:
        print("Failed to set up the environment.")

if __name__ == '__main__':
    setup_environment()
