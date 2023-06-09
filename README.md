# HELLO

使用docker build新映像

```
docker build -t cuttool .
```

```
docker run -idt --name cuttool -v %cd%:/app cuttool
```

```
docker exec -it cuttool /bin/bash
```


確保在input_dir內有放置圖片，以便進行主物件圖像剪輯
執行python cutV4.py 可自行帶入--size參數，設定預裁切大小
預設為416 * 416

```
python cutV4.py
```
"# CutTool_withyolov5" 
