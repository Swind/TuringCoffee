
這是測試用的 Cookbook 資料，
顯示在這邊的是此 Cookbook 的 Description

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: home
Command: refill
```

``` heat
Water Tank: 60 degress C
```
## 定點注水

在原點 (0, 0) 注水 20 ml

每次以 0.01 ml 的水量擠出

``` fixed_point
Coordinates: (0, 0)
High: 80 mm to 80 mm
Total Water: 20 ml
Extrudate: 0.01 ml/step
```

## 繞圓注水

繞半徑 1 cm 的圓注水 40 ml

在注水過程中，會從 80 mm 升高到 70 mm

每 1 mm 吐出 0.1 ml 的水

每個吐水的點間距 0.01 mm

``` circle
Radius: 1 cm
Total Water: 40 ml
High: 80 mm to 70 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.01 mm
```

## 等待預浸

等待預浸時間 30 秒

``` operations
Command: home
Command: refill
Command: wait 30s
```

# Step 2: 沖煮

## 繞圓注水

繞半徑 1 cm 的圓注水 40 ml, 每 1 mm 吐出 0.1 ml 的水

``` circle
Radius: 1 cm
Total Water: 40 ml
High: 80 mm to 70 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.01 mm
```

## 螺旋注水

從離中心 1 cm 的地方開始使用螺旋注水

繞行 5 圈

``` spiral
Radius: 1 cm to 2 cm
High: 80 mm to 70 mm
Cylinder: 5
Point interval: 0.01 mm
Feedrate: 80 mm/min
Extrudate: 0.1 ml/mm
```

## 螺旋注水 - 繞回中心

從離中心 2 cm 的地方使用螺旋注水往回繞

繞行 5 圈

``` spiral
Radius: 2 cm to 1 cm
High: 80 mm to 80 mm
Cylinder: 5
Point interval: 0.01 mm
Feedrate: 80 mm/min
Extrudate: 0.1 ml/mm
```

## 繞圓注水

繞半徑 1 cm 的圓注水 40 ml, 每 1 mm 吐出 0.1 ml 的水

``` circle
Radius: 1 cm
Total Water: 40 ml
High: 80 mm to 70 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.01 mm
```

## 結束

``` operations
Command: home
Command: refill
```

``` heat
Water Tank: 0 degress C
```
