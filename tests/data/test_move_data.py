# -*- coding:utf-8 -*-

data = """
# Step 1: 測試移動

move 的功能是移動到某個定點，並且吐水

move 的指令移動速度預設為 3000 mm/min

## 範例 1 - 快速移動 Z 軸

移動到高度 170 mm, Feedrate 3000 mm/min

``` move
    Z: 170 mm
```

## 範例 2 - 快速移動 Z 軸

移動到 X: 10 mm, Y: 10 mm, Z: 270 mm, Feedrate 3000 mm/min

``` move
    X: 10 mm
    Y: 10 mm
    Z: 170 mm
```
"""
