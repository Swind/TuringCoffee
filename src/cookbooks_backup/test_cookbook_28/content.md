
水量校正

# Step 1: 注水


## 事前準備

``` operations
Command: Home
```

##移動到下面

``` move
Z: 135 mm
Feedrate: 500 mm/min
```

## 定點注水

``` fixed_point
Coordinates: (0, 0)
High: 135 mm to 135 mm
Total Water: 100 ml
Extrudate: 0.028 ml/step
Feedrate： 200 mm/min
```

## 結束

``` operations
Command: Home
Command: refill
```
