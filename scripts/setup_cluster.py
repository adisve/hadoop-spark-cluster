import os
import logging
import subprocess
from utils.docker_utils import DockerUtils
from halo import Halo


class SparkHadoopSetup:
    """
    Class to set up the Spark and Hadoop environment

    Attributes
    ----------
    network_name : str
        name of the Docker network
    hadoop_container_dir : str
        path to the directory containing the docker-compose.yml file

    Methods
    -------
    create_spark_hadoop_network()
        Creates a Docker network for the Spark and Hadoop containers to communicate
    start_container(container_dir)
        Starts the Docker containers
    setup_environment()
        Sets up the Spark and Hadoop environment
    """
    def __init__(self):
        self.network_name = "shared-spark-hadoop-network"
        self.hadoop_container_dir = "hadoop-spark-cluster"

    def create_spark_hadoop_network(self):
        spinner = Halo(text=f"Checking for existing network: {self.network_name}")
        spinner.start()
        existing_networks = subprocess.run(
            ["docker", "network", "ls"], capture_output=True, text=True
        )

        if self.network_name in existing_networks.stdout:
            spinner.succeed(f"Network {self.network_name} already exists")
            return True

        spinner.text = f"Creating shared network: {self.network_name}"
        try:
            subprocess.run(["docker", "network", "create", self.network_name], check=True)
            spinner.succeed(f"Network {self.network_name} created")
            return True
        except subprocess.CalledProcessError as e:
            spinner.fail(f"Error creating network: {e}")
            logging.error(f"Error during network creation: {e}")
            return False

    def start_container(self, container_dir):
        docker_compose_cmd = DockerUtils.get_docker_compose_cmd()
        command = docker_compose_cmd + ["up", "-d"]
        spinner = Halo(text=f"Starting containers in {container_dir}", spinner="dots")
        spinner.start()
        os.chdir(container_dir)
        try:
            subprocess.run(command, check=True)
            os.chdir("..")
            spinner.succeed("Containers started")
            return True
        except Exception as e:
            spinner.fail(f"Error starting Docker containers: {e}")
            return False

    def setup_environment(self):
        if self.create_spark_hadoop_network() and self.start_container(self.hadoop_container_dir):
            print("Environment setup completed successfully.")
        else:
            print("Failed to set up the environment.")

if __name__ == "__main__":
    setup = SparkHadoopSetup()
    setup.setup_environment()
