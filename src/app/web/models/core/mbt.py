from flask import Flask, render_template as real_render_template
from datetime import datetime
from app.web.models.core.di import main_injection


class Mbt(Flask):
    """
    This wrapper class for Flask App
    """

    @main_injection
    def __init__(self) -> None:
        # * Initialize the Flask app
        super().__init__(__name__)


def render_template(*args, **kwargs):
    # Get the current year
    year = datetime.now().year
    # Return the render template
    return real_render_template(*args, **kwargs, year=year)
