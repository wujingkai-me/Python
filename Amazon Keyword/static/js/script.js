const vm = new Vue({
  el: "#root",
  data: {
    // b: "",
    array: [],
    process: "还未开始",
    filename: "",
    isProgress: false,
    filter: {
      filterElement: ""
    }
  },
  methods: {
    isEmpty(element) {
      return element.length == 0 ? false : true;
    },
    getData() {
      const COUNTRY = {
        "英国": "AMAZON_CO_UK",
        "法国": "AMAZON_FR",
        "德国": "AMAZON_DE",
        "意大利": "AMAZON_IT", 
        "西班牙": "AMAZON_ES" 
      };
      let countrySelect = document.querySelector(".countrySelect")
      let options = countrySelect.querySelectorAll("option");
      let whoSelected = null;

      for(let i = 0; i < options.length; i ++) {
        if(options[i].selected) whoSelected = options[i].innerText
      }

      whoSelected = COUNTRY[whoSelected]
      console.log(whoSelected, "被选择")
      


      // this.isProgress = true
      let isSync = true // 是否异步调用
      for (let i = "a".charCodeAt(); i <= "z".charCodeAt(); i++) {
        let xmlhttp = new XMLHttpRequest();
        let value = keyword.value + " " + String.fromCharCode(i);
        
        xmlhttp.open("GET", "/getkeyword/" + value + "/" + whoSelected, isSync);
        xmlhttp.send();
        
        // 回调函数
        xmlhttp.onreadystatechange = (i) => {
          if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            this.process = String.fromCharCode(i);
            this.array.push(eval("(" + xmlhttp.responseText + ")"));
          }
        };
      }
      // this.process = false;
    },

    Clear() {
      this.array = []
      // // 消除重复
      // // for(let i = 0; i < this.array.length; i++) {
      // //   this.array[i] = this.array[i].filter(function(item, index, self) {
      // //     return self.indexOf(item) == index;
      // //   });
      // // }
      
      // // 过滤
      // var F = this.filter.filterElement;
      // for(let i = 0; i < this.array.length; i++) {
      //   for(let j = 0; j < this.array[i].length; j++) {
      //     if(this.array[i][j][0].includes(F)){
      //       let temp = this.array[i];
      //       temp[j][0] = this.array[i][j][0].replace(F, "").trim();
      //       this.$set(this.array, i, temp);
      //     }
      //   }
      // }
    },

    Download() {
      // let xmlhttp = new XMLHttpRequest();
      // xmlhttp.open("GET", "/Download/" + this.array, true);
      // xmlhttp.send();
      // xmlhttp.onreadystatechange = () => {
      //   if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      //     console.log("Download Success")
      //   }
      // }
      if(this.filename != ""){
        this.tableToPdf(document.getElementById("grid", this.filename))
      }else {
        this.tableToPdf(document.getElementById("grid", "content.pdf"))
      }
    },
    tableToPdf(dom, saveFilename) {
      html2canvas(
      //这个是想要导出的DOM元素的id
          dom,
          {
              dpi: 400,//导出pdf清晰度
              onrendered: function (canvas) {
                  var contentWidth = canvas.width;
                  var contentHeight = canvas.height;
    
                  //一页pdf显示html页面生成的canvas高度;
                  var pageHeight = contentWidth / 592.28 * 841.89;
                  //未生成pdf的html页面高度
                  var leftHeight = contentHeight;
                  //pdf页面偏移
                  var position = 0;
                  //html页面生成的canvas在pdf中图片的宽高（a4纸的尺寸[595.28,841.89]）
                  var imgWidth = 595.28;
                  var imgHeight = 592.28 / contentWidth * contentHeight;
    
                  var pageData = canvas.toDataURL('image/jpeg', 1.0);
                  var pdf = new jsPDF('', 'pt', 'a4');
    
                  //有两个高度需要区分，一个是html页面的实际高度，和生成pdf的页面高度(841.89)
                  //当内容未超过pdf一页显示的范围，无需分页
                  if (leftHeight < pageHeight) {
                      pdf.addImage(pageData, 'JPEG', 0, 0, imgWidth, imgHeight);
                  } else {
                      while (leftHeight > 0) {
                          pdf.addImage(pageData, 'JPEG', 0, position, imgWidth, imgHeight)
                          leftHeight -= pageHeight;
                          position -= 841.89;
                          //避免添加空白页
                          if (leftHeight > 0) {
                              pdf.addPage();
                          }
                      }
                  }
                  pdf.save(saveFilename);
              },
              //背景设为白色（默认为黑色）
              background: "#fff"
          })
    },
  }

});



