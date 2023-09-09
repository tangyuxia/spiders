var Crypto = require('crypto-js')
hash = {
    'sha1': function (a) {
        return Crypto.SHA1(a).toString()
    },
    'sha256': function (a) {
        return Crypto.SHA256(a).toString()
    },
    'md5': function (a) {
        return Crypto.MD5(a).toString()
    }
}
var cn_time = new Date();
go = {
    "bts": ["1679579129.628|0|XfM", "oxhlqFrt3ILwl8FUWQGvXA%3D"],
    "chars": "nVLlCpXuzlObhYOoJJENgL",
    "ct": "8360f3186fae9f2119b0b69a05bd608a971db59d052673f850397b507d535fe9",
    "ha": "sha256",
    "tn": "__jsl_clearance_s",
    "vt": "3600",
    "wt": "1500"
}
function cookie(go) {
    var data_len = go['chars']['length'];
    for (var i = 0; i < data_len; i++) {
        for (var j = 0; j < data_len; j++) {
            var cookie1 = go['bts'][0] + go['chars']['substr'](i, 1) + go['chars']['substr'](j, 1) + go['bts'][1];
            if (hash[go['ha']](cookie1) == go['ct']) {
                return [cookie1, new Date() - cn_time];
            }
        }
    }
}
// coo = cookie(go)
// console.log(coo)

// hash 加密的结果  必定是40位才会相等
// hash方法 就是算法  而且还是根据前端传的 ha 来确定用什么算法进行加密
// 加速乐有三种  sha1 md5 sha256