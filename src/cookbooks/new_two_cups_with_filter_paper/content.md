
2杯量的咖啡 加 濾紙

# Step 1: 預浸

預浸需要 80 度 60ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: Home
```

## 先行吐水維持溫度

``` move
Z: 255 mm
Feedrate: 1000 mm/min
```

``` waste_water
Cold Water: 50 ml
Hot Water: 50 ml
```

``` mix_temperature
Total Water: 30 ml
Temperature: 55 degress C
```

## 噴頭上移方便換杯

``` move
Feedrate: 1000 mm/min
```
``` move
Z: 255 mm
```

## 快速移動到255 mm

``` move
Feedrate: 1000 mm/min
```

``` move
Z: 255 mm
```

## 開始預浸

定點注水 30 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 255 mm to 255 mm
Total Water: 5 ml
Extrudate: 0.1 ml/step
Point interval: 1.0 mm
Temperature: 55 degress C
```

繞圓 35 ml

``` spiral_total_water
Radius: 0.1 cm to 2.2 cm
High: 255 mm to 255 mm
Cylinder: 8
Total Water: 35 ml
Total Time: 35 s
Point interval: 1.0 mm
```

``` mix_temperature
Total Water: 1 ml
Temperature: 65 degress C
```

## 等待 30s

``` wait
Time: 30s
```

``` move
Feedrate: 120 mm/min
```

``` mix_temperature
Total Water: 50 ml
Temperature: 65 degress C
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 3.5 cm
High: 255 mm to 255 mm
Cylinder: 8
Total Water: 170 ml
Total Time: 60 s
Point interval: 1.0 mm
```

## 螺旋注水 - 繞回中心

從離中心 3.5 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral_total_water
Radius: 3.5 cm to 0.1 cm
High: 255 mm to 255 mm
Cylinder: 8
Total Water: 170 ml
Total Time: 60 s
Point interval: 1.0 mm
```

## HOME

``` operations
Command: Home
```
