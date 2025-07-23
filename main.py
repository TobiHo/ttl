"""Entry point for the TTL game collection."""

import argparse


def main() -> None:
    """Start one of the available games.

    Currently only ``pong`` is implemented. Additional games can be passed as an
    argument, but will result in an error message.
    """

    parser = argparse.ArgumentParser(description="TTL Game Collection")
    parser.add_argument(
        "game",
        nargs="?",
        default="pong",
        help="Name of the game to start (default: pong)",
    )
    args = parser.parse_args()

    if args.game == "pong":
        from games import pong
        pong.run()
    else:
        print(f"Unknown game '{args.game}'. Available games: pong")

if __name__ == '__main__':
    main()
