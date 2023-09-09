const jsdom = require("jsdom");
const {JSDOM} = jsdom;

const resourceLoader = new jsdom.ResourceLoader({
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
});

const html = `<!DOCTYPE html><p>Hello world</p>`;
const dom = new JSDOM(html, {
    url: "https://www.mps.gov.cn/n2253534/n2253535/index.html",
    referrer: "https://www.mps.gov.cn/n2253534/n2253535/index.html",
    contentType: "text/html",
    resources: resourceLoader,
});

window = dom.window

// window = global;
document = window.document;
// cookie=document.cookie


const params = {
    location: {
        // hash: "",
        // host: "www.mps.gov.cn",
        // hostname: "www.toutiao.com",
        // // href: "https://www.toutiao.com",
        // // origin: "https://www.toutiao.com",
        // pathname: "/",
        // port: "",
        // protocol: "https:",
        // search: "",

         "ancestorOrigins": {},
        "href": "http://www.customs.gov.cn/customs/302427/302442/gljdhcd/index.html",
        "origin": "http://www.customs.gov.cn/",
        "protocol": "https:",
        "host": "m.tujia.com",
        "hostname": "m.tujia.com",
        "port": "",
        "pathname": "/customs/302427/302442/gljdhcd/index.html",
        "search": "",
        "hash": ""
    },
    navigator: {
        appCodeName: "Mozilla",
        appName: "Netscape",
        appVersion: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        cookieEnabled: true,
        deviceMemory: 8,
        doNotTrack: null,
        hardwareConcurrency: 4,
        language: "zh-CN",
        languages: ["zh-CN", "zh"],
        maxTouchPoints: 0,
        onLine: true,
        platform: "MacIntel",
        product: "Gecko",
        productSub: "20030107",
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        vendor: "Google Inc.",
        vendorSub: "",
        webdriver: false
    },
};

Object.assign(global, params);


function L(t) {
    void 0 === t && (t = 28),
        t = t || 10;
    for (var e = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz0123456789", n = e.length, o = "", r = 0; r < t; r++)
        o += e.charAt(Math.floor(Math.random() * n));
    return o
}
function set(t, e, n, o, r) {
    var i = ""
        , s = ""
        , a = "";
    if (o) {
        // var c = document.location.hostname.match(x)
        var c = document.location.hostname.match('/[a-z0-9][a-z0-9\\-]+\\.[a-z\\.]{2,6}$/i')
            , u = c ? c[0] : "";
        i = u ? "; domain=." + u : ""
    }
    if (n) {
        var f = new Date;
        f.setTime(f.getTime() + 24 * n * 60 * 60 * 1e3),
            s = "; expires=" + f.toGMTString()
    }
    r && (a = "; secure");
    // var p = t + "=" + encodeURIComponent(e) + s + "; path=/" + i + a;
    var p = t + "=" + encodeURIComponent(e) + s  + i + a;
    return document.cookie = p
}

function fas_session_id(){
    return (t = function (t) {
        return void 0 === t && (t = 28),
        L(t) + (new Date).getTime()
    }(),
        // S.set(M, t),
        // b.set(M, t)
        set("_fas_session_id", t)
)
}
// console.log(fas_session_id())
