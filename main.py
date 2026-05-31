# https://github.com/ariWeinberg/CRUD_shapes_manager
import app_logger
from app_logger import get_logger
import dynamic_shapes
import dynamic_actions
from app import App

def main():
    """
    The main enterypoint to this program

    This is the main function and entrypoint to the app
    It is trying to be as minimalistic as possible and keep the rest OOP.
    """
    try:
        logger = get_logger("root")
        app = App()
        app.run()
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[4D\nbye... (got ctrl + c)\nexiting now.")
