"""
ASGI config for lemon_ninja project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# # Import Tortoise ORM initialization functions
# from config.tortoise_init import init_tortoise, close_tortoise
# from config.settings import TORTOISE_ORM

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

# # Initialize Tortoise ORM
# async def main():
#     await init_tortoise(TORTOISE_ORM)

# # It's important to run the Tortoise ORM initialization
# # within the same event loop that Django uses for async operations.
# # Django's get_asgi_application() sets up an event loop when it's first called.
# # We can hook into this by overriding the application object with a wrapper
# # that initializes Tortoise ORM before starting the Django application.

# original_application = application

# async def application_wrapper(scope, receive, send):
#     if scope['type'] == 'lifespan':
#         async def startup():
#             await init_tortoise(TORTOISE_ORM)

#         async def shutdown():
#             await close_tortoise()

#         # Simple lifespan handling
#         while True:
#             message = await receive()
#             if message['type'] == 'lifespan.startup':
#                 await startup()
#                 await send({'type': 'lifespan.startup.complete'})
#             elif message['type'] == 'lifespan.shutdown':
#                 await shutdown()
#                 await send({'type': 'lifespan.shutdown.complete'})
#                 return
#     else:
#         await original_application(scope, receive, send)

# application = application_wrapper
