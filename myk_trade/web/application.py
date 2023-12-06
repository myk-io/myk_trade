from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, UJSONResponse
from fastapi.staticfiles import StaticFiles
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin
from piccolo_api.session_auth.endpoints import session_login, session_logout
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from piccolo_api.shared.auth.junction import AuthenticationBackendJunction
from piccolo_api.token_auth.middleware import PiccoloTokenAuthProvider, TokenAuthBackend
from piccolo_api.token_auth.tables import TokenAuth
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount

from myk_trade.db.models import transactions
from myk_trade.logging import configure_logging
from myk_trade.web.api.router import api_router
from myk_trade.web.lifetime import register_shutdown_event, register_startup_event
from myk_trade.web.ui.router import ui_router

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="myk_trade",
        version=metadata.version("myk_trade"),
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        routes=[
            # to use Piccolo admin:
            Mount(
                "/admin/",
                create_admin(
                    tables=[
                        BaseUser,
                        TokenAuth,
                        transactions.CurrencyModel,
                        transactions.WalletModel,
                        transactions.TransactionModel,
                    ],
                ),
                site_name="Myk Trade Admin",
            ),
            # Session Auth login:
            Mount(
                "/login/",
                session_login(redirect_to="/"),
            ),
            # Session Auth logout:
            Mount(
                "/logout/",
                session_logout(redirect_to="/"),
            ),
        ],
        middleware=[
            Middleware(
                AuthenticationMiddleware,
                backend=AuthenticationBackendJunction(
                    backends=[
                        TokenAuthBackend(
                            token_auth_provider=PiccoloTokenAuthProvider(),
                        ),
                        SessionsAuthBackend(
                            allow_unauthenticated=True,
                            admin_only=False,
                        ),
                    ],
                ),
            ),
        ],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    # Main router for the API.
    app.include_router(
        router=api_router,
        prefix="/api",
    )

    # Ui using Jinja2.
    app.mount(
        "/ui",
        ui_router,
        name="ui",
    )

    @app.get("/")
    async def _index():
        return RedirectResponse(url="/ui/")

    # Adds session login endpoint.
    # app.mount("/login", jwt_login)

    return app
