
三杯量的咖啡

# Step 1: 預浸

預浸需要 75 度 60ml 的水，注水結束之後等待 20 秒

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
Feedrate: 800 mm/min
Z: 225 mm
```

``` move
Feedrate: 300 mm/min
Z: 225 mm
```

``` fixed_point
Coordinates: (0, 0)
High: 225 mm to 225 mm
Total Water: 150 ml
Extrudate: 1 ml/step
Feedrate: 200 mm/min
```

``` move
Feedrate: 500 mm/min
```

``` move
Z: 225 mm
```

``` wait
Time: 20s
```

``` move
Feedrate: 300 mm/min
```

``` move
Z: 225 mm
```

## 開始預浸

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 225 mm to 225 mm
Total Water: 15 ml
Extrudate: 1 ml/step
Feedrate: 120 mm/min
```

``` spiral_total_water
Radius: 0.1 cm to 1.2 cm
High: 225 mm to 225 mm
Cylinder: 6
Total Water: 35 ml
Point interval: 0.1 mm
```

## 等待 20s

``` wait
Time: 20s
```

``` move
Feedrate: 120 mm/min
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 3.5 cm
High: 225 mm to 225 mm
Cylinder: 8
Total Water: 225 ml
Point interval: 0.1 mm
```

## 螺旋注水 - 繞回中心

從離中心 3.5 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral_total_water
Radius: 3.5 cm to 0.1 cm
High: 225 mm to 225 mm
Cylinder: 8
Total Water: 225 ml
Point interval: 0.1 mm
```

## HOME

``` operations
Command: Home
```
