"""Data parser for blender dataset"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Type

import imageio
import numpy as np
import torch

from nerfstudio.cameras.cameras import Cameras, CameraType
from nerfstudio.data.dataparsers.base_dataparser import (
    DataParser,
    DataParserConfig,
    DataparserOutputs,
)
from nerfstudio.data.scene_box import SceneBox
from nerfstudio.utils.colors import get_color
from nerfstudio.utils.io import load_from_json


@dataclass
class FourDVDataParserConfig(DataParserConfig):
    """D-NeRF dataset parser config"""

    _target: Type = field(default_factory=lambda: FourDV)
    """target class to instantiate"""
    data: Path = Path("data/blender/fox")
    """Directory specifying location of data."""
    scale_factor: float = 1.0
    """How much to scale the camera origins by."""
    alpha_color: str = "white"
    """alpha color of background"""


@dataclass
class FourDV(DataParser):
    """FourDV Dataset"""

    config: FourDVDataParserConfig
    includes_time: bool = True

    def __init__(self, config: FourDVDataParserConfig):
        super().__init__(config=config)
        self.data: Path = config.data
        self.scale_factor: float = config.scale_factor
        self.alpha_color = config.alpha_color

    def _generate_dataparser_outputs(self, split="train"):
        if self.alpha_color is not None:
            alpha_color_tensor = get_color(self.alpha_color)
        else:
            alpha_color_tensor = None

        meta = load_from_json(self.data / f"transforms_{split}.json")
        image_filenames = []
        poses = []
        times = []
        camera_ids = []
        for frame in meta["frames"]:
            fname = self.data / Path(frame["file_path"].replace("./", "") + ".png")
            image_filenames.append(fname)
            poses.append(np.array(frame["transform_matrix"]))
            times.append(frame["time"])
            camera_id = frame["file_path"].split("/")[-1]
            camera_ids.append(int(camera_id))
        poses = np.array(poses).astype(np.float32)
        times = torch.tensor(times, dtype=torch.float32)

        img_0 = imageio.imread(image_filenames[0])
        image_height, image_width = img_0.shape[:2]
        camera_angle_x = float(meta["camera_angle_x"])
        focal_length = 0.5 * image_width / np.tan(0.5 * camera_angle_x)

        cx = image_width / 2.0
        cy = image_height / 2.0
        camera_to_world = torch.from_numpy(poses[:, :3])  # camera to world transform

        # in x,y,z order
        camera_to_world[..., 3] *= self.scale_factor
        scene_box = SceneBox(aabb=torch.tensor([[-5.0, -5.0, -5.0], [5.0, 5.0, 5.0]], dtype=torch.float32))

        # metadata
        num_cameras = len(set(camera_ids))
        num_frames = len(poses) // num_cameras
        metadata = {"camera_ids": camera_ids, "num_cameras": num_cameras, "num_frames": num_frames}

        # noise
        # time_noise = torch.normal(mean=0., std=0.1/(num_frames-1), size=(num_cameras,), dtype=torch.float32)
        # times = times + time_noise[camera_ids]
        # print(f"time_noise = {time_noise}")

        print(times)

        cameras = Cameras(
            camera_to_worlds=camera_to_world,
            fx=focal_length,
            fy=focal_length,
            cx=cx,
            cy=cy,
            camera_type=CameraType.PERSPECTIVE,
            times=times,
        )

        dataparser_outputs = DataparserOutputs(
            image_filenames=image_filenames,
            cameras=cameras,
            alpha_color=alpha_color_tensor,
            scene_box=scene_box,
            dataparser_scale=self.scale_factor,
            metadata=metadata,
        )

        return dataparser_outputs
