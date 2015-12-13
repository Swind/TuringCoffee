
吐水測試

# Step 1: 吐水


## 事前準備 

``` operations
Command: Home
```

``` mix_temperature
Total Water: 50 ml
Temperature: 65 degress C
```

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
