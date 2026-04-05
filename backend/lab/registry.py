from backend.lab.infophyzx.experiment_lab import router as infophyzx_experiment_router

def register_lab(app):
    app.include_router(infophyzx_experiment_router)
