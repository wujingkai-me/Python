# 如何运行
下载`AmazonToolsSets.zip` 在其中可以找到`__arun.bat` 目录运行 `__arun.bat` 可以在桌面找到 `app` 和 `bullet` 目录
- `app` 运行主程序 你可以在 浏览器中运行`localhost:5000` 将其打开
- `bullet` 存放需要查询的五点描述更加快捷的管理方式

# JavaScript脚本

获得一个Amazon页面中的五点描述，需要和插件配合
```javascript
javascript:
var w = window.open("feture.html");
var feturesItems = document.querySelectorAll(".feature-item-p");
for(var item of feturesItems){     
  var p = item.querySelectorAll("p");
       for(var fetures of p){
             w.document.write(fetures.innerText.trim() + "<br/>");     
       } 
}
