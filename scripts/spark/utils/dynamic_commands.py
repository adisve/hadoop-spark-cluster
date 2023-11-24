import subprocess


def get_docker_compose_cmd():
    command = ["uname", "-m"]
    architecture = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    match architecture:
        case "x86_64":
            return ["docker-compose"]
        case "arm64":
            return ["docker-compose"]
        case "amd64":
            return ["docker", "compose"]
        case _:
            raise Exception("Unsupported architecture")