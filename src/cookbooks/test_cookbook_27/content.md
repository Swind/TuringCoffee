
這是測試用的 Cookbook 資料，
顯示在這邊的是此 Cookbook 的 Description

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備

``` operations
Command: home
```

## 繞圓注水

繞半徑 1 cm 的圓注水 40 ml

在注水過程中，會從 80 mm 升高到 70 mm

每 1 mm 吐出 0.1 ml 的水

每個吐水的點間距 0.1 mm

``` circle
Radius: 1 cm
Total Water: 40 ml
High: 240 mm to 250 mm
Feedrate： 80 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.1 mm
```