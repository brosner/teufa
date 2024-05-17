import gunicorn.app.base

from .app import create_app


class Application(gunicorn.app.base.BaseApplication):

    def __init__(self, options=None):
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return create_app()
