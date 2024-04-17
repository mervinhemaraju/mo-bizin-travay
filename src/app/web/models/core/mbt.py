from flask import Flask
from app.web.models.core.di import main_injection


class Mbt(Flask):
    """
    This wrapper class for Flask App
    """

    @main_injection
    def __init__(self) -> None:
        # * Initialize the Flask app
        super().__init__(__name__)
