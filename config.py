from flask.cli import load_dotenv


class Config:
    """
    Configuration manager for the Julius Baer API client.

    Reads configuration from a YAML file and overrides values
    with environment variables when available.
    """

    def __init__(self, config_file_path: str = "config.yaml"):
        """
        Initialize the configuration manager.

        Args:
            config_file_path: Path to the YAML configuration file. Defaults to "config.yaml".
        """
        # Load environment variables from .env file if it exists
        load_dotenv()