// ==UserScript==
// @name         super bili
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       mk39
// @require      https://unpkg.com/ajax-hook@2.0.2/dist/ajaxhook.min.js
// @include      *//www.bilibili.com/bangumi/play/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';
    //输入你的域名
    var url = ''
    ah.proxy({
        onRequest: (config, handler) => {
            if (/^[\s\S]*\/\/api.bilibili.com\/pgc\/player\/web\/playurl[\s\S]*/.test(config.url)) {
                config.url = `https://${url}/pgc/player/web/playurl?` + config.url.split("?")[1]
            }
            handler.next(config);
        },
        onError: (err, handler) => {
            console.log(err.type)
            handler.next(err)
        },
        onResponse: (response, handler) => {
            if (`https://${url}/pgc/player/web/playurl` == response.config.url) {
                if (response.response.code == -10043) {
                    alert(response.response.message)
                }
            } else if (/^[\s\S]*\/\/api.bilibili.com\/pgc\/review\/user[\s\S]*/.test(response.config.url)) {
                var view = JSON.parse(response.response)
                if (view.result.media.type_name == '电影') {
                    alert('电影如果只有6分钟请尝试切换1080p+,如果只有480p就切换自动画质然后会出现1080p+，再切换1080p+')
                }
            }
            handler.next(response)
        }
    })
    function getCookie(cookie_name) {
        var allcookies = document.cookie;
        var cookie_pos = allcookies.indexOf(cookie_name);
        if (cookie_pos != -1) {
            cookie_pos = cookie_pos + cookie_name.length + 1;
            var cookie_end = allcookies.indexOf(";", cookie_pos);
            if (cookie_end == -1) {
                cookie_end = allcookies.length;
            }
            var value = unescape(allcookies.substring(cookie_pos, cookie_end));
        }
        return value;
    }

    //感谢解除区域限制脚本
    function modiy(name, modifyFn) {
        const name_origin = `${name}_origin`
        window[name_origin] = window[name]
        let value = undefined
        Object.defineProperty(window, name, {
            configurable: true,
            enumerable: true,
            get: () => {
                return value
            },
            set: (val) => {
                value = modifyFn(val)
            }
        })
        if (window[name_origin]) {
            window[name] = window[name_origin]
        }
    }
    function vip2() {
        modiy('__INITIAL_STATE__', (value) => {
            for (let ep of [value.epInfo, ...value.epList]) {
                if (ep.epStatus === 13) {
                    ep.epStatus = 2
                }
            }
            return value
        })
    }
    function vip() {
        modiy('__PGC_USERSTATE__', (value) => {
            if (value) {
                value.pay = 1
                value.area_limit = 0
                value.vip_info.status = 1
                value.vip_info.due_date = 1888953600000
                value.vip_info.type = 2
            }
            console.log(value)
            return value
        })
    }
    vip()
    vip2()
})();