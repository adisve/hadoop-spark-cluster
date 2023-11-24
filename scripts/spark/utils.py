import subprocess


class Utils:
    """
    Utility methods

    Methods
    -------
    get_docker_compose_cmd()
        Returns the appropriate docker-compose command based on the architecture
    dataframe_to_html_with_css(df, css_path="/css/default-styles.css")
        Returns the HTML data of a Pandas DataFrame with CSS styling
    """
    @staticmethod
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
    
    @staticmethod
    def dataframe_to_html_with_css(df, css_path="/css/default-styles.css"):
        html_data = df.to_html()
        html_data_with_css = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                {html_data}
            </body>
            </html>
        """
        return html_data_with_css