
2杯量的咖啡 加 濾紙

# Step 1: 預浸

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
Total Water: 40 ml
Temperature: 75 degress C
```

## 移動一下
``` move
Z: 260 mm
Feedrate: 1000 mm/min
```


## 開始預浸


``` move
Feedrate: 60 mm/min
```

``` fixed_point
Coordinates: (0, 0)
High: 255 mm to 255 mm
Total Water: 10 ml
Extrudate: 0.1 ml/step
Point interval: 1.0 mm
Temperature: 75 degress C
```

繞圓 35 ml

``` spiral_total_water
Radius: 0.1 cm to 3.2 cm
High: 255 mm to 255 mm
Cylinder: 2
Total Water: 50 ml
Total Time: 35 s
Point interval: 1.0 mm
```

``` mix_temperature
Total Water: 1 ml
Temperature: 80 degress C
```

## 預浸等待時間

``` wait
Time: 10s
```

``` move
Feedrate: 120 mm/min
```

``` mix_temperature
Total Water: 50 ml
Temperature: 80 degress C
```

``` wait
Time: 10s
```



# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3.5 cm 的地方開始使用螺旋注水

``` spiral_total_water
Radius: 0.1 cm to 1.2 cm
High: 255 mm to 255 mm
Cylinder: 6
Total Water: 60 ml
Total Time: 36 s
Point interval: 1.0 mm
```


``` spiral_total_water
Radius: 1.2 cm to 2.8 cm
High: 255 mm to 255 mm
Cylinder: 8
Total Water: 200 ml
Total Time: 96 s
Point interval: 1.0 mm
```



``` spiral_total_water
Radius: 2.8 cm to 0.1 cm
High: 255 mm to 255 mm
Cylinder: 4
Total Water: 100 ml
Total Time: 48 s
Point interval: 1.0 mm
```


## HOME

``` operations
Command: Home
```
