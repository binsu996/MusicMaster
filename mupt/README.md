```
# 运行服务
serve run mupt:app

# 发起请求
curl 'http://localhost:8000/' -X 'POST' -H 'Content-Type: application/json; charset=UTF-8'  -d '{"prompt":"X:1<n>L:1/8<n>Q:1/8=200<n>M:4/4<n>K:Cmin<n>| C2:", "tokens_
to_generate":4096}'
```

整体而言，效果还可以，但是无法控制生成合格的MIDI，难以在产品中使用。