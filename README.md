# ctrl.engine

#### A general purpose robotics engine

## Installation
Python:
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
```
