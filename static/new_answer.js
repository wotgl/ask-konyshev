 var WS = function() {
    ws = new WebSocket("ws://127.0.0.1:8888/test");

    ws.onopen = function() {

        ws.send(JSON.stringify({'url': window.location.href}))

        answer_template = localStorage.getItem("answer_template");
        if (answer_template == null) {
            ws.send(JSON.stringify({'answer_template': 0}))
        }

    };
    ws.onmessage = function (evt) {
        // console.log(evt.data);

        // John Resig Template
        (function(){
            var cache = {};
            this.tmpl = function tmpl(str, data){
            var fn = !/\W/.test(str) ?
              cache[str] = cache[str] ||
                tmpl(document.getElementById(str).innerHTML) :
              new Function("obj",
                "var p=[],print=function(){p.push.apply(p,arguments);};" +               
                "with(obj){p.push('" +               
                str
                  .replace(/[\r\t\n]/g, " ")
                  .split("<%").join("\t")
                  .replace(/((^|%>)[^\t]*)'/g, "$1\r")
                  .replace(/\t=(.*?)%>/g, "',$1,'")
                  .split("\t").join("');")
                  .split("%>").join("p.push('")
                  .split("\r").join("\\'")
              + "');}return p.join('');");
            return data ? fn( data ) : fn;
            };
            })();






        try {
            var json_data = JSON.parse(evt.data);
        } catch(e) {
            return;
        }

        var key = Object.keys(json_data)[0];

        switch (key) {
            case "new_answer":
                console.log("get new_answer");
                var new_answer = json_data[key];
                console.log(new_answer);

                // Check page_id
                var re = /http:\/\/[a-z0-9A-Z.\/]+question\/\d+\/\?page=(\d+)/;
                var url = window.location.href;
                var matches = url.match(re);

                if (matches == null) {
                    if (new_answer['page_id'] != "1")
                        return
                } else {
                    var check_page_id = matches[1];
                    if (check_page_id != new_answer['page_id'])
                        return
                }

                // Get div template
                var template = localStorage.getItem("answer_template");

                // Check like/dislike btns
                var check_auth = $('[name=csrfmiddlewaretoken]').val();
                if (check_auth)
                    new_answer['auth'] = "";
                else
                    new_answer['auth'] = "disabled";

                // Check correct_btn
                var check_question_user = $("#question_author").attr("value");
                var check_user = $("#username").attr("value");

                if (check_question_user == check_user)
                    new_answer['check_author'] = "";
                else
                    new_answer['check_author'] = "none";

                // Use John Resig Template
                var res = tmpl(template, new_answer)
                $("#answers_list").append(res);

                // Update foo() <=> like/dislike btns
                foo();
                break;
            case "answer_template":
                console.log("get answer_template");
                localStorage.setItem("answer_template", json_data[key]);
                break;
            default:
                break;
        }

    };
    ws.onclose = function (evt) {
        console.log("onclose");
    };
 }

window.onload = WS;
 