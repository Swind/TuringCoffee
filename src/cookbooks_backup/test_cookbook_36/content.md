
測試最小螺旋

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備 

``` operations
Command: Home
```

## 加熱溫度到80

``` heat
Water Tank: 80 degress C
```

## 往下移動

``` move
Z: 175 mm
Feedrate: 200 mm/min
```

## 先行吐水維持溫度

``` fixed_point
Coordinates: (0, 0)
High: 175 mm to 175 mm
Total Water: 150 ml
Extrudate: 1 ml/step
Feedrate: 200 mm/min
```

## 噴頭上移方便換杯

``` move
Feedrate: 1000 mm/min
```
``` move
Z: 190 mm
```

## 等待20秒方便換杯

``` wait
Time: 20s
```

## 快速移動到175 mm

``` move
Feedrate: 1000 mm/min
```

``` move
Z: 175 mm
```

## 開始預浸

定點注水 5 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 170 mm to 170 mm
Total Water: 5 ml
Extrudate: 0.1 ml/step
```

小螺旋 0.1 -> 0.5 cm

``` spiral
Radius: 0.1 cm to 0.5 cm
High: 170 mm to 170 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.1 ml/mm
```

小螺旋 0.1 -> 0.5 cm

``` spiral
Radius: 0.1 cm to 0.5 cm
High: 170 mm to 170 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.1 ml/mm
```

# Step 2: 沖煮

## 繞半徑 0.1 -> 2 cm 的螺旋

``` spiral
Radius: 0.1 cm to 2 cm
High: 175 mm to 175 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.1 ml/mm
```

## 螺旋注水 - 繞回中心

從離中心 2 cm 的地方使用螺旋注水往回繞
繞行 5 圈

``` spiral
Radius: 2 cm to 0.1 cm
High: 175 mm to 175 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.1 ml/mm
```

## HOME

``` wait
Time: 2s
```

``` operations
Command: Home
```
