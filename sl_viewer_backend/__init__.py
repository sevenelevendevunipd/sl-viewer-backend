from spectree import SpecTree
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

spec = SpecTree("starlette")

from .api import ApiMount  # noqa: E402

app = Starlette(
    debug=True,
    routes=[
        ApiMount
    ],
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"])],
)

spec.register(app)
