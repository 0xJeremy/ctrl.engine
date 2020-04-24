<div align="center">
  <img src="https://raw.githubusercontent.com/0xJeremy/ctrl.engine/master/graphics/Logo.png">
</div>

#### A general purpose robotics engine

## Installation

[Python](https://pypi.org/project/ctrl.engine/):
```
pip install ctrl.engine
```

This library is tested with Ubuntu 19.04 and Python 3.7.5. It was developed specifically for use with robotics using a Raspberry Pi.

## Modules

```python
from ctrlengine.controllers import PID

from ctrlengine.filters import simple_moving_average
from ctrlengine.filters import exponentially_weighted_moving_average

from ctrlengine.sensors import camera

from ctrlengine.tools import xbox_ctrl

from ctrlengine.util import logger

from ctrlengine.ai import face_detection
from ctrlengine.ai import image_classificatoin
from ctrlengine.ai import object_detection
from ctrlengine.ai import pose_detection

from ctrlengine.ai.cloud_vision import cloud_vision
from ctrlengine.ai.text_to_speech import text_to_speech

from ctrlengine.ai.azure_vision import azure_vision
```
