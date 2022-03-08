from pathlib import Path
class Models:
    def __init__(self):
        self.models = self.get_models()
        self.default = self.models[0].name
    def get_models(self):
        wd = Path.cwd()
        models = wd/'models'
        models = [i for i in models.iterdir()]
        return models 
