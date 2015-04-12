
注水降溫

# Step 1: 注水


## 事前準備

``` operations
Command: Home
```

##移動到下面

``` move
Z: 165 mm
Feedrate: 500 mm/min
```

## 定點注水

在原點 (0, 0) 注水 200 ml
每次以 5 ml 的水量擠出

``` fixed_point
Coordinates: (0, 0)
High: 165 mm to 165 mm
Total Water: 200 ml
Extrudate: 5 ml/step
Feedrate： 400 mm/min
```

## 結束

``` operations
Command: Home
Command: refill
```