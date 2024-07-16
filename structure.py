import os
import sys
from dotenv import load_dotenv
from typing import Optional

from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener
from griptape.structures import Agent


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ

def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        print(
            """
              ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
              This environment variable is required when running in Griptape Cloud for authorization.
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key

def run_griptape_agent(input: str, event_driver: Optional[GriptapeCloudEventListenerDriver]):
    structure = Agent(
        event_listeners=[EventListener(driver=event_driver)],
    )
    structure.run(input)

input=sys.argv[1]
# Are we running this program in a managed environment (i.e., the Skatepark
# emulator or Griptape Cloud), or completely local (such as within an IDE)?
if is_running_in_managed_environment():
    # In the managed environment, our environment variables are provided for us.
    # We need an event driver to communicate events from this program back
    # to our host.
    # The event driver requires a URL to the host.
    # When running in Skatepark or Griptape Cloud, this value is automatically
    # provided to you in the environment variable GT_CLOUD_BASE_URL. You can
    # override this value by specifying your own for
    # GriptapeCloudEventListenerDriver.base_url .
    event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
else:
    # If running completely local, such as within an IDE, load environment vars.
    # This is done automatically for you when the Structure is run within the
    # Skatepark emulator or as a Structure on Griptape Cloud.
    load_dotenv()

    # We don't need an event driver if we're testing the program in an IDE.
    event_driver = None

run_griptape_agent(input, event_driver)
