from api.routes import remote_ops

app.include_router(remote_ops.router, prefix="/remote", tags=["RemoteOps"])