from python_json_config import ConfigBuilder
from python_json_config.validators import is_unreserved_port


class Config:
    def __init__(self, path: str = "./config.json", builder: ConfigBuilder = ConfigBuilder()):
        self.path = path
        self.builder = builder
        self.config = None

        # Validate data types
        self.builder.validate_field_type('server.host', str)
        self.builder.validate_field_type('server.port', int)
        self.builder.validate_field_type('server.version', str)

        # Validate data values
        self.builder.validate_field_value('server.port', is_unreserved_port)

        # Parse if all valid
        self.config = self.builder.parse_config(self.path)

    def get_config(self):
        self.config = self.builder.parse_config(self.path)
        return self.config
