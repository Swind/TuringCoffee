
3杯量的咖啡 + 金屬濾網 + 75 度

# Step 1: 預浸

## 事前準備 

``` operations
Command: Home
```

## 先行吐水維持溫度

``` move
Z: 280 mm
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

## 開始預浸

定點注水 30 ml

``` move
Feedrate: 120 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 280 mm to 280 mm
Total Water: 10 ml
Extrudate: 0.1 ml/step
Point interval: 1.0 mm
```

繞圓 50 ml

``` spiral_total_water
Radius: 0.1 cm to 4.5 cm
High: 280 mm to 280 mm
Cylinder: 10
Total Water: 50 ml
Total Time: 35 s
Point interval: 1.0 mm
```

``` mix_temperature
Total Water: 1 ml
Temperature: 65 degress C
```

## 等待 40s

``` wait
Time: 40s
```

``` move
Feedrate: 120 mm/min
```

``` mix_temperature
Total Water: 50 ml
Temperature: 75 degress C
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 4.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 4.5 cm
High: 280 mm to 280 mm
Cylinder: 15
Total Water: 260 ml
Total Time: 80 s
Point interval: 1.0 mm
```

## 螺旋注水 - 繞回中心

從離中心 4.5 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral_total_water
Radius: 4.5 cm to 0.1 cm
High: 280 mm to 280 mm
Cylinder: 15
Total Water: 260 ml
Total Time: 80 s
Point interval: 1.0 mm
```

## HOME

``` operations
Command: Home
```
