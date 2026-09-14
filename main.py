import typer

from config import CONFIG, Config
from game import Game


def main(
    window_width: int | None = typer.Option(None, "--window-width"),
    window_height: int | None = typer.Option(None, "--window-height"),
    fullscreen: bool = typer.Option(False, "--fullscreen"),
    fps: int | None = typer.Option(None, "--fps"),
    speed: int | None = typer.Option(None, "--speed"),
    tile_size: int | None = typer.Option(None, "--tile-size"),
    gui_font_size: int | None = typer.Option(None, "--gui-font-size"),
    gui_text_color: str | None = typer.Option(None, "--gui-text-color"),
):
    config = CONFIG.parse_cli(
        window_width=window_width,
        window_height=window_height,
        fullscreen=fullscreen,
        fps=fps,
        speed=speed,
        tile_size=tile_size,
        gui_font_size=gui_font_size,
        gui_text_color=gui_text_color,
    )

    run_game(config)


def run_game(config: Config):
    with Game(config) as game:
        game.run()


if __name__ == "__main__":
    typer.run(main)
