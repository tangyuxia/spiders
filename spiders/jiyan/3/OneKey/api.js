const express = require('express');
//导入js逆向中需要调用的函数
const {w1,w2} = require('./jiyan_jiyan');
const app = express();

app.get('/getw1', (req, res) => {
    const str = req.query.str;
    const dict=JSON.parse(str)

    const result = w1(dict);
    console.log(result)
  res.send(result);
  // res.json(result);
});

app.get('/getw2', (req, res) => {
    const gt = req.query.gt;
    const challenge = req.query.challenge;
    const c = req.query.c;
    const s = req.query.s;
    const nn = req.query.nn;

    const result = w2(gt, challenge, c, s,nn);
    console.log(result)
  res.send(result);
  // res.json(result);
});

//服务器监听端口3000
app.listen(3000, '127.0.0.1',() => {
  console.log('Server listening on port 3000');
});

// dd=JSON.stringify({'gt': '389a2c6a640dfd83ff7aa338f0c01fd2', 'challenge': '65f4a267b7bd0ca695f267f9e046834d', 'offline': 'false', 'new_captcha': 'true', 'product': 'float', 'width': '300px', 'https': 'true', 'api_server': 'apiv6.geetest.com', 'protocol': 'https://', 'type': 'fullpage', 'static_servers': ['static.geetest.com/', 'dn-staticdown.qbox.me/'], 'beeline': '/static/js/beeline.1.0.1.js', 'voice': '/static/js/voice.1.2.3.js', 'click': '/static/js/click.3.0.9.js', 'fullpage': '/static/js/fullpage.9.1.4.js', 'slide': '/static/js/slide.7.9.0.js', 'geetest': '/static/js/geetest.6.0.9.js', 'aspect_radio': {'slide': 103, 'click': 128, 'voice': 128, 'beeline': 50}, 'cc': 12, 'ww': 'true'})
// console.log(dd)

// 访问地址
// http://127.0.0.1:3000/getw1?str='{"gt":"389a2c6a640dfd83ff7aa338f0c01fd2","challenge":"65f4a267b7bd0ca695f267f9e046834d","offline":"false","new_captcha":"true","product":"float","width":"300px","https":"true","api_server":"apiv6.geetest.com","protocol":"https://","type":"fullpage","static_servers":["static.geetest.com/","dn-staticdown.qbox.me/"],"beeline":"/static/js/beeline.1.0.1.js","voice":"/static/js/voice.1.2.3.js","click":"/static/js/click.3.0.9.js","fullpage":"/static/js/fullpage.9.1.4.js","slide":"/static/js/slide.7.9.0.js","geetest":"/static/js/geetest.6.0.9.js","aspect_radio":{"slide":103,"click":128,"voice":128,"beeline":50},"cc":12,"ww":"true"}'

// http://127.0.0.1:3000/getw2?gt=389a2c6a640dfd83ff7aa338f0c01fd2&challenge=e52fcfdb457089ebebb51090147d5ab2&c=[12, 58, 98, 36, 43, 95, 62, 15, 12]&s=732e7e41&nn=534f867c541db2ac