
一杯量的咖啡

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: home
```

## 快速移動到 240 mm

``` move
Z: 165 mm
Feedrate: 1000 mm/min
```

## 開始預浸

定點注水 5 ml

``` move
Feedrate: 80 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 165 mm to 165 mm
Total Water: 5 ml
Extrudate: 0.1 ml/step
```

繞圓 15 ml

``` circle
Radius: 1 cm
Total Water: 15 ml
High: 165 mm to 165 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.1 mm
```

## 等待 40s

``` wait
Time: 5s
```

# Step 2: 沖煮

## 繞半徑 1cm 的圓

``` circle
Radius: 1 cm
Total Water: 45 ml
High: 165 mm to 165 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.1 mm
```

## 螺旋注水 1cm -> 2cm

從離中心 1 cm 的地方向 2 cm 開始使用螺旋注水

繞行 5 圈

``` spiral
Radius: 1 cm to 2 cm
High: 165 mm to 165 mm
Cylinder: 10
Point interval: 0.1 mm
Feedrate: 80 mm/min
Extrudate: 0.1 ml/mm
```

## 繞半徑 1cm 的圓

``` circle
Radius: 1 cm
Total Water: 45 ml
High: 165 mm to 165 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.1 mm
```