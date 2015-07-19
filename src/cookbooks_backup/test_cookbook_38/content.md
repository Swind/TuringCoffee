新三杯量的咖啡

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
Feedrate: 500 mm/min
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
Z: 350 mm
```

## 等待20秒方便換杯

``` wait
Time: 20s
```

## 開始預浸

定點注水 5 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 290 mm to 290 mm
Total Water: 15 ml
Extrudate: 0.1 ml/step
```

繞圓 15 ml

``` spiral
Radius: 0.1 cm to 2 cm
High: 290 mm to 290 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.1 ml/mm
```

## 等待 40s

``` wait
Time: 40s
```

``` move
Feedrate: 120 mm/min
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3 cm 的地方開始使用螺旋注水

``` spiral
Radius: 0.1 cm to 3 cm
High: 295 mm to 295 mm
Cylinder: 16
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.15 ml/mm
```

## 螺旋注水 - 繞回中心

從離中心 3 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral
Radius: 3 cm to 0.1 cm
High: 295 mm to 295 mm
Cylinder: 16
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.15 ml/mm
```

## HOME

``` operations
Command: Home
```
