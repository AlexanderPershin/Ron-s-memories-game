from pydantic import BaseModel, Field


class Config(BaseModel):
    window_width: int = Field(default=800, gt=0, le=3840)
    window_height: int = Field(default=600, gt=0, le=2160)

    fullscreen: bool = False

    fps: int = Field(default=60, ge=30, le=240)

    speed: int = Field(default=300, gt=0)

    tile_size: int = Field(default=128, gt=0, le=256)

    gui_font_size: int = Field(default=24, gt=0, le=200)
    gui_text_color: str = Field(default="#ffffffcc")

    def parse_cli(self, **overrides) -> Config:
        updates = {k: v for k, v in overrides.items() if v is not None}
        current_data = self.model_dump()
        current_data.update(updates)
        return Config(**current_data)


CONFIG = Config()
