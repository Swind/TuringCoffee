
測試螺旋總時間

# Step 1: 預浸

預浸需要 80 度 60ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: Home
```

``` move
Feedrate: 2000 mm/min
Z: 240 mm
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 3.5 cm
High: 240 mm to 240 mm
Cylinder: 12
Total Water: 200 ml
Total Time: 60 s
Point interval: 1.0 mm
Temperature: 40 degress C
```

## HOME

``` operations
Command: Home
```
