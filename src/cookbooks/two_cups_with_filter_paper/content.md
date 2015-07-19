
2杯量的咖啡 加 濾紙

# Step 1: 預浸

預浸需要 80 度 60ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: Home
```

## 先行吐水維持溫度

``` move
Z: 180 mm
Feedrate: 1000 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 180 mm to 180 mm
Total Water: 150 ml
Extrudate: 1 ml/step
Feedrate: 200 mm/min
```

## 噴頭上移方便換杯

``` move
Feedrate: 1000 mm/min
```
``` move
Z: 180 mm
```

## 等待20秒方便換杯

``` wait
Time: 20s
```

## 快速移動到180 mm

``` move
Feedrate: 1000 mm/min
```

``` move
Z: 180 mm
```

## 開始預浸

定點注水 30 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 180 mm to 180 mm
Total Water: 5 ml
Extrudate: 0.1 ml/step
Point interval: 0.1 mm
```

繞圓 35 ml

``` spiral_total_water
Radius: 0.1 cm to 1.7 cm
High: 180 mm to 180 mm
Cylinder: 8
Total Water: 35 ml
Total Time: 40 s
Point interval: 0.14 mm
```

## 等待 12s

``` wait
Time: 12s
```

``` move
Feedrate: 120 mm/min
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 3.5 cm
High: 180 mm to 180 mm
Cylinder: 8
Total Water: 170 ml
Total Time: 60 s
Point interval: 0.3 mm
```

## 螺旋注水 - 繞回中心

從離中心 3.5 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral_total_water
Radius: 3.5 cm to 0.1 cm
High: 180 mm to 180 mm
Cylinder: 8
Total Water: 170 ml
Total Time: 60 s
Point interval: 0.3 mm
```

## HOME

``` operations
Command: Home
```
