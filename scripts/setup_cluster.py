import os
import logging
import subprocess
from spark.utils.dynamic_commands import get_docker_compose_cmd
from halo import Halo

class SparkHadoopSetup:
    def __init__(self):
        self.network_name = "spark-hadoop-network"
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
        docker_compose_cmd = get_docker_compose_cmd()
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
