
三杯量的咖啡

# Step 1: 預浸

預浸需要 80 度 60ml 的水，注水結束之後等待 20 秒

## 事前準備 

``` operations
Command: Home
```

加熱溫度到80

##``` heat
##Water Tank: 75 degress C
##```

往下移動

``` move
Feedrate: 500 mm/min
Z: 175 mm
```

##``` fixed_point
##Coordinates: (0, 0)
##High: 175 mm to 175 mm
##Total Water: 150 ml
##Extrudate: 1 ml/step
##Feedrate: 200 mm/min
##```

``` move
Feedrate: 500 mm/min
```

``` move
Z: 190 mm
```

##``` wait
##Time: 20s
##```

``` move
Feedrate: 500 mm/min
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
Feedrate: 200 mm/min
```

``` spiral
Radius: 0.1 cm to 2 cm
High: 170 mm to 170 mm
Cylinder: 12
Point interval: 0.1 mm
Feedrate: 200 mm/min
Extrudate: 0.2 ml/mm
```

## 等待 40s

``` wait
Time: 20s
```

``` move
Feedrate: 200 mm/min
```

# Step 2: 沖煮

## 螺旋注水

從離中心 0.1 cm -> 3 cm 的地方開始使用螺旋注水

``` spiral
Radius: 0.1 cm to 3.5 cm
High: 170 mm to 170 mm
Cylinder: 12
Point interval: 0.1 mm
Feedrate: 200 mm/min
Extrudate: 0.2 ml/mm
```

## 螺旋注水 - 繞回中心

從離中心 3 cm -> 0.1 cm 的地方使用螺旋注水往回繞

``` spiral
Radius: 3.5 cm to 0.1 cm
High: 170 mm to 170 mm
Cylinder: 12
Point interval: 0.1 mm
Feedrate: 200 mm/min
Extrudate: 0.2 ml/mm
```


## HOME

``` operations
Command: Home
```
