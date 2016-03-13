# rr-texture-manager

Usage:
```python
import pymel.core as pm
from rrTextureManager import RRTextureManager

tm = RRTextureManager()
texture_nodes = pm.ls(type='file')

for n in texture_nodes:
  tm.add_node(n)

tm.change_all_paths('/tmp')
```
