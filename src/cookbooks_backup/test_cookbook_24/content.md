
一杯量的咖啡

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備 

``` operations
Command: Home
```

## 加熱溫度到80

``` heat
Water Tank: 75 degress C
```

## 往下移動


``` move
Z: 160 mm
Feedrate: 500 mm/min
```


## 先行吐水維持溫度

``` fixed_point
Coordinates: (0, 0)
High: 160 mm to 160 mm
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
Z: 160 mm
```

## 開始預浸

定點注水 5 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 160 mm to 160 mm
Total Water: 5 ml
Extrudate: 0.1 ml/step
```

繞圓 15 ml

``` spiral
Radius: 0.1 cm to 1.2 cm
High: 160 mm to 160 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Total Water: 7.5 ml
Extrudate: 0.2 ml/mm
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

從離中心 0.1 cm -> 2 cm 的地方開始使用螺旋注水

``` spiral
Radius: 0.1 cm to 2 cm
High: 160 mm to 160 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.2 ml/mm
```

## 螺旋注水 - 繞回中心

從離中心 2 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral
Radius: 2 cm to 0.1 cm
High: 160 mm to 160 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.2 ml/mm
```

## HOME

``` operations
Command: Home
```
