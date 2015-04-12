
測三軸

# Step 1: 預浸

預浸需要 60 度 20ml 的水，注水結束之後等待 20 秒

## 事前準備 

``` operations
Command: Home
```

## 加熱溫度到80

``` heat
Water Tank: 21 degress C
```

## 往下移動

## 快速移動到175 mm

``` move
Z: 175 mm
Feedrate: 200 mm/min
```

``` move
Feedrate: 200 mm/min
Z: 150 mm 
```

繞圓 15 ml

``` circle
Radius: 1 cm
Total Water: 15 ml
High: 175 mm to 175 mm
Feedrate： 120 mm/min
Extrudate: 0.1 ml/mm
Point interval: 0.1 mm
```


``` operations
Command: Home
```