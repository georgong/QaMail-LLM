$(document).ready(function() {
    const msgerForm = $(".msger-inputarea");
    const msgerInput = $(".msger-input");
    const msgerChat = $(".msger-chat");
    var htmlContent = ""
  
    const BOT_IMG = "static/image/girl1_1.png";
    const PERSON_IMG = "static/image/user1.png";
    const BOT_NAME = "BOT";
    const PERSON_NAME = "我";
    var count = 0;
    const inital_html_frame = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Email Assistant</title>
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 20px 0;
            text-align: center;
            border-bottom: 5px solid #0056b3;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0;
        }
        .header img {
            width: 50px;
            height: 50px;
            margin-right: 10px;
            vertical-align: middle;
        }
        .content {
            padding: 50px 20px;
            text-align: center;
        }
        .content p {
            font-size: 1.2rem;
            color: #6c757d;
        }
        .footer {
            background-color: #343a40;
            color: white;
            text-align: center;
            padding: 10px 0;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Email Assistant</h1>
    </div>
    <div class="content">
        <p>Welcome to the AI Email Assistant, making your email communication smarter and more efficient!</p>
    </div>
    <div class="footer">
        <p>&copy; 2023 AI Email Assistant. All rights reserved.</p>
    </div>
</body>
</html>
    `
// 在JavaScript中添加以下代码
let settings = {
    timeFilter: 0,      // 0:1年, 1:半年, 2:月, 3:实时
    temperature: 0.7,
    keywordFilter: "",
    startdate: "",
    enddate: "",
    selfRAG: false
};

const button = document.getElementById('selfrag');
        let isLightGray = true; // 初始状态为浅灰色

        button.addEventListener('click', function() {
            if (isLightGray) {
                button.style.backgroundColor = '#87CEEB'; // 切换为浅蓝色
            } else {
                button.style.backgroundColor = '#cccccc'; // 切换回浅灰色
            }
            isLightGray = !isLightGray; // 切换状态
            settings.selfRAG = !settings.selfRAG;
        });


// 设置面板切换
$("#settingsToggle").click(() => {
    $("#settingsPanel").toggleClass("hidden");
});

// 关闭按钮
$(".close-btn").click(() => {
    resetSettings();
    $("#settingsPanel").addClass("hidden");
});

// 时间过滤滑块


// Temperature滑块
$("#temperature").on("input", function() {
    $("#tempValue").text(this.value);
});

// 应用设置
$("#applySettings").click(() => {
    settings.temperature = parseFloat($("#temperature").val());
    settings.keywordFilter = $("#keywordFilter").val();
    settings.startdate = document.getElementById("startDate").value
    settings.enddate = document.getElementById("endDate").value
    $("#settingsPanel").addClass("hidden");
});

// Self-RAG切换
    document.getElementById('html-iframe').srcdoc = inital_html_frame
    // const startRecognitionButton = document.getElementById('startRecognition');
    // const speechToTextArea = document.getElementById('speechToText');

    // startRecognitionButton.addEventListener('click', () => {
    //     if ('webkitSpeechRecognition' in window) {
    //         const recognition = new webkitSpeechRecognition();
    //         recognition.continuous = false;
    //         recognition.interimResults = false;
    //         recognition.lang = 'zh-CN'; // 设置语言为中文，可以根据需要更改
  
    //         recognition.onresult = (event) => {
    //             const transcript = event.results[0][0].transcript;
    //         };
  
    //         recognition.onerror = (event) => {
    //             console.error('语音识别错误:', event.error);
    //         };
  
    //         recognition.start();
    //     } else {
    //         alert('您的浏览器不支持Web Speech API，请使用Chrome或Firefox浏览器。');
    //     }
    // });

    function resetSettings() {
        $("#startDate").val(""); // 清空日期选择器
        $("#endDate").val("");
        $("#temperature").val("0.7"); // 恢复默认值 0.7
        $("#tempValue").text("0.7"); // 更新显示值
        $("#keywordFilter").val(""); // 清空文本框
    }
  
    msgerForm.on("submit", async function(event) {
        event.preventDefault();
        /**/
        if (event.originalEvent && event.originalEvent.submitter) {
            const senderElement = event.originalEvent.submitter;
    
            // Prevent form submission if the clicked element is not the "Send" button
            if (!$(senderElement).hasClass("msger-send-btn")) {
                return;
            }
        }
        /**/
        const msgText = msgerInput.val();
        if (!msgText) return;
        appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
        msgerInput.val("");
        appendMessage(BOT_NAME, BOT_IMG, "left", "");
        console.log(settings)
  
        // 发送消息到服务器并获取响应
        const res = await fetch('/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ "user_info": msgText, "setting": settings})
        });
  
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let botResponse = '';
  
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            const text = decoder.decode(value);
            botResponse += text;
            document.getElementById(count + "lefttext").innerText = botResponse;
        }
  
        // 获取文档链接
        const retrieveRes = await fetch('/retrieve', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ "user_info": msgText })
        });
  
        const retrieveData = await retrieveRes.json();
        console.log(retrieveData.result)
        const dict_list = retrieveData.result;
        const maxInitialDisplay = 3; // 初始显示的高亮文字数量
        let toggleTexts = [];

        for (let i=0;i<dict_list.length;i++) {
            console.log("run")
            var toggleText = document.createElement('div');
            toggleText.innerText = dict_list[i]["subject"] + ": " + dict_list[i]["score"];
            toggleText.style.cursor = "pointer";
            toggleText.style.marginTop = "10px";
            toggleText.style.color = "blue";
            toggleText.style.textDecoration = "underline"; 
            toggleText.onclick = function() {
                htmlContent = dict_list[i]["html_content"]
                const iframe = document.getElementById('html-iframe');
                iframe.srcdoc = htmlContent;
            };
            toggleTexts.push(toggleText);
        }

        // 初始显示前3条高亮文字
        for (let i = 0; i < Math.min(maxInitialDisplay, toggleTexts.length); i++) {
            document.getElementById(count + "lefttext").appendChild(toggleTexts[i]);
        }

        // 添加“展开”按钮
        var expandButton = document.createElement('div');
        expandButton.innerText = "展开";
        expandButton.style.cursor = "pointer";
        expandButton.style.marginTop = "10px";
        expandButton.style.color = "blue";
        expandButton.position = count
        expandButton.style.textDecoration = "underline";
        console.log(toggleTexts)
        expandButton.onclick = function() {
            if (expandButton.innerText === "展开") {
                // 展开所有高亮文字
                for (let i = maxInitialDisplay; i < toggleTexts.length; i++) {
                    console.log(toggleTexts[i])
                    const highlight_word = toggleTexts[i]
                    const copy_count = this.position
                    document.getElementById(copy_count + "lefttext").insertBefore(highlight_word,this);
                }
                expandButton.innerText = "折叠";
            } else {
                // 折叠所有高亮文字
                for (let i = maxInitialDisplay; i < toggleTexts.length; i++) {
                    const copy_count = this.position
                    document.getElementById(copy_count + "lefttext").removeChild(toggleTexts[i]);
                }
                expandButton.innerText = "展开";
            }
        };
        document.getElementById(count + "lefttext").appendChild(expandButton);

        count++;
    });
  
    function appendMessage(name, img, side, text) {
        const msgHTML = `
            <div class="msg ${side}-msg">
                <div class="msg-img" style="background-image: url(${img})"></div>
  
                <div class="msg-bubble">
                    <div class="msg-info">
                        <div class="msg-info-name">${name}</div>
                        <div class="msg-info-time">${formatDate(new Date())}</div>
                    </div>
  
                    <div class="msg-text" id = "${count}${side}text">${text}</div>
                </div>
            </div>
        `;
  
        msgerChat.append(msgHTML);
        msgerChat.scrollTop(msgerChat.prop("scrollHeight"));
    }
  
    function formatDate(date) {
        const h = "0" + date.getHours();
        const m = "0" + date.getMinutes();
  
        return `${h.slice(-2)}:${m.slice(-2)}`;
    }
});