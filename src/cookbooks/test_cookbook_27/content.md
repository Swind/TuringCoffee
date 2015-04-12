
三杯量的咖啡

# Step 1: 預浸

預浸需要 80 度 60ml 的水，注水結束之後等待 20 秒

## 事前準備 

``` operations
Command: Home
```

加熱溫度到80

``` heat
Water Tank: 80 degress C
```

往下移動

``` move
Feedrate: 800 mm/min
Z: 175 mm
```

``` move
Feedrate: 300 mm/min
Z: 180 mm
```

``` fixed_point
Coordinates: (0, 0)
High: 175 mm to 175 mm
Total Water: 150 ml
Extrudate: 1 ml/step
Feedrate: 200 mm/min
``

``` move
Feedrate: 500 mm/min
```

``` move
Z: 190 mm
```

``` wait
Time: 20s
```

``` move
Feedrate: 300 mm/min
```

``` move
Z: 175 mm
```

## 開始預浸

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 170 mm to 170 mm
Total Water: 15 ml
Extrudate: 1 ml/step
Feedrate: 120 mm/min
```

``` circle
Radius: 1 cm
Total Water: 45 ml
High: 175 mm to 175 mm
Feedrate： 120 mm/min
Extrudate: 1 ml/mm
Point interval: 0.1 mm
```

## 等待 40s

``` wait
Time: 40s
```

``` move
Feedrate: 120 mm/min
```

# Step 2: 沖煮

## 繞半徑 1 cm 的圓

``` circle
Radius: 1.5 cm
Total Water: 135 ml
High: 175 mm to 175 mm
Feedrate： 120 mm/min
Extrudate: 0.3 ml/mm
Point interval: 0.1 mm
```

## 螺旋注水

``` spiral
Radius: 1.5 cm to 3 cm
High: 175 mm to 175 mm
Cylinder: 6
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.3 ml/mm
Total Water: 135 ml
```

## 螺旋注水 - 繞回中心

``` spiral
Radius: 3 cm to 1.5 cm
High: 175 mm to 175 mm
Cylinder: 6
Total Water: 135 ml
Point interval: 0.1 mm
Feedrate: 120 mm/min
Extrudate: 0.3 ml/mm
```

## 繞半徑 1 cm 的圓

``` circle
Radius: 1.5 cm
Total Water: 135 ml
High: 175 mm to 175 mm
Feedrate： 120 mm/min
Extrudate: 0.3 ml/mm
Point interval: 0.1 mm
```

## HOME

``` operations
Command: Home
```
