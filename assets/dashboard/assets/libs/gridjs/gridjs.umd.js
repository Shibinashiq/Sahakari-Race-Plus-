!function (t, e) {
    "object" == typeof exports && "undefined" != typeof module ? e(exports) : "function" == typeof define && define.amd ? define(["exports"], e) : e((t || self).gridjs = {})
}(this, function (t) {
    function e(t, e) {
        for (var n = 0; n < e.length; n++) {
            var r = e[n];
            r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
        }
    }

    function n(t, n, r) {
        return n && e(t.prototype, n), r && e(t, r), t
    }

    function r() {
        return (r = Object.assign || function (t) {
            for (var e = 1; e < arguments.length; e++) {
                var n = arguments[e];
                for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r])
            }
            return t
        }).apply(this, arguments)
    }

    function i(t, e) {
        t.prototype = Object.create(e.prototype), t.prototype.constructor = t, o(t, e)
    }

    function o(t, e) {
        return (o = Object.setPrototypeOf || function (t, e) {
            return t.__proto__ = e, t
        })(t, e)
    }

    function s(t) {
        if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
        return t
    }

    function a(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r
    }

    function u(t, e) {
        var n = "undefined" != typeof Symbol && t[Symbol.iterator] || t["@@iterator"];
        if (n) return (n = n.call(t)).next.bind(n);
        if (Array.isArray(t) || (n = function (t, e) {
            if (t) {
                if ("string" == typeof t) return a(t, e);
                var n = Object.prototype.toString.call(t).slice(8, -1);
                return "Object" === n && t.constructor && (n = t.constructor.name), "Map" === n || "Set" === n ? Array.from(t) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? a(t, e) : void 0
            }
        }(t)) || e && t && "number" == typeof t.length) {
            n && (t = n);
            var r = 0;
            return function () {
                return r >= t.length ? {done: !0} : {done: !1, value: t[r++]}
            }
        }
        throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
    }

    var l, c, p, h, f, d, _ = {}, m = [], g = /acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord|itera/i;

    function v(t, e) {
        for (var n in e) t[n] = e[n];
        return t
    }

    function y(t) {
        var e = t.parentNode;
        e && e.removeChild(t)
    }

    function b(t, e, n) {
        var r, i, o, s = arguments, a = {};
        for (o in e) "key" == o ? r = e[o] : "ref" == o ? i = e[o] : a[o] = e[o];
        if (arguments.length > 3) for (n = [n], o = 3; o < arguments.length; o++) n.push(s[o]);
        if (null != n && (a.children = n), "function" == typeof t && null != t.defaultProps) for (o in t.defaultProps) void 0 === a[o] && (a[o] = t.defaultProps[o]);
        return w(t, a, r, i, null)
    }

    function w(t, e, n, r, i) {
        var o = {
            type: t,
            props: e,
            key: n,
            ref: r,
            __k: null,
            __: null,
            __b: 0,
            __e: null,
            __d: void 0,
            __c: null,
            __h: null,
            constructor: void 0,
            __v: null == i ? ++l.__v : i
        };
        return null != l.vnode && l.vnode(o), o
    }

    function P(t) {
        return t.children
    }

    function k(t, e) {
        this.props = t, this.context = e
    }

    function S(t, e) {
        if (null == e) return t.__ ? S(t.__, t.__.__k.indexOf(t) + 1) : null;
        for (var n; e < t.__k.length; e++) if (null != (n = t.__k[e]) && null != n.__e) return n.__e;
        return "function" == typeof t.type ? S(t) : null
    }

    function C(t) {
        var e, n;
        if (null != (t = t.__) && null != t.__c) {
            for (t.__e = t.__c.base = null, e = 0; e < t.__k.length; e++) if (null != (n = t.__k[e]) && null != n.__e) {
                t.__e = t.__c.base = n.__e;
                break
            }
            return C(t)
        }
    }

    function x(t) {
        (!t.__d && (t.__d = !0) && p.push(t) && !N.__r++ || f !== l.debounceRendering) && ((f = l.debounceRendering) || h)(N)
    }

    function N() {
        for (var t; N.__r = p.length;) t = p.sort(function (t, e) {
            return t.__v.__b - e.__v.__b
        }), p = [], t.some(function (t) {
            var e, n, r, i, o, s;
            t.__d && (o = (i = (e = t).__v).__e, (s = e.__P) && (n = [], (r = v({}, i)).__v = i.__v + 1, I(s, i, r, e.__n, void 0 !== s.ownerSVGElement, null != i.__h ? [o] : null, n, null == o ? S(i) : o, i.__h), U(n, i), i.__e != o && C(i)))
        })
    }

    function E(t, e, n, r, i, o, s, a, u, l) {
        var c, p, h, f, d, g, v, y = r && r.__k || m, b = y.length;
        for (n.__k = [], c = 0; c < e.length; c++) if (null != (f = n.__k[c] = null == (f = e[c]) || "boolean" == typeof f ? null : "string" == typeof f || "number" == typeof f || "bigint" == typeof f ? w(null, f, null, null, f) : Array.isArray(f) ? w(P, {children: f}, null, null, null) : f.__b > 0 ? w(f.type, f.props, f.key, null, f.__v) : f)) {
            if (f.__ = n, f.__b = n.__b + 1, null === (h = y[c]) || h && f.key == h.key && f.type === h.type) y[c] = void 0; else for (p = 0; p < b; p++) {
                if ((h = y[p]) && f.key == h.key && f.type === h.type) {
                    y[p] = void 0;
                    break
                }
                h = null
            }
            I(t, f, h = h || _, i, o, s, a, u, l), d = f.__e, (p = f.ref) && h.ref != p && (v || (v = []), h.ref && v.push(h.ref, null, f), v.push(p, f.__c || d, f)), null != d ? (null == g && (g = d), "function" == typeof f.type && null != f.__k && f.__k === h.__k ? f.__d = u = F(f, u, t) : u = T(t, f, h, y, d, u), l || "option" !== n.type ? "function" == typeof n.type && (n.__d = u) : t.value = "") : u && h.__e == u && u.parentNode != t && (u = S(h))
        }
        for (n.__e = g, c = b; c--;) null != y[c] && ("function" == typeof n.type && null != y[c].__e && y[c].__e == n.__d && (n.__d = S(r, c + 1)), M(y[c], y[c]));
        if (v) for (c = 0; c < v.length; c++) H(v[c], v[++c], v[++c])
    }

    function F(t, e, n) {
        var r, i;
        for (r = 0; r < t.__k.length; r++) (i = t.__k[r]) && (i.__ = t, e = "function" == typeof i.type ? F(i, e, n) : T(n, i, i, t.__k, i.__e, e));
        return e
    }

    function T(t, e, n, r, i, o) {
        var s, a, u;
        if (void 0 !== e.__d) s = e.__d, e.__d = void 0; else if (null == n || i != o || null == i.parentNode) t:if (null == o || o.parentNode !== t) t.appendChild(i), s = null; else {
            for (a = o, u = 0; (a = a.nextSibling) && u < r.length; u += 2) if (a == i) break t;
            t.insertBefore(i, o), s = o
        }
        return void 0 !== s ? s : i.nextSibling
    }

    function D(t, e, n) {
        "-" === e[0] ? t.setProperty(e, n) : t[e] = null == n ? "" : "number" != typeof n || g.test(e) ? n : n + "px"
    }

    function R(t, e, n, r, i) {
        var o;
        t:if ("style" === e) if ("string" == typeof n) t.style.cssText = n; else {
            if ("string" == typeof r && (t.style.cssText = r = ""), r) for (e in r) n && e in n || D(t.style, e, "");
            if (n) for (e in n) r && n[e] === r[e] || D(t.style, e, n[e])
        } else if ("o" === e[0] && "n" === e[1]) o = e !== (e = e.replace(/Capture$/, "")), e = e.toLowerCase() in t ? e.toLowerCase().slice(2) : e.slice(2), t.l || (t.l = {}), t.l[e + o] = n, n ? r || t.addEventListener(e, o ? A : L, o) : t.removeEventListener(e, o ? A : L, o); else if ("dangerouslySetInnerHTML" !== e) {
            if (i) e = e.replace(/xlink[H:h]/, "h").replace(/sName$/, "s"); else if ("href" !== e && "list" !== e && "form" !== e && "tabIndex" !== e && "download" !== e && e in t) try {
                t[e] = null == n ? "" : n;
                break t
            } catch (t) {
            }
            "function" == typeof n || (null != n && (!1 !== n || "a" === e[0] && "r" === e[1]) ? t.setAttribute(e, n) : t.removeAttribute(e))
        }
    }

    function L(t) {
        this.l[t.type + !1](l.event ? l.event(t) : t)
    }

    function A(t) {
        this.l[t.type + !0](l.event ? l.event(t) : t)
    }

    function I(t, e, n, r, i, o, s, a, u) {
        var c, p, h, f, d, g, b, w, S, C, x, N = e.type;
        if (void 0 !== e.constructor) return null;
        null != n.__h && (u = n.__h, a = e.__e = n.__e, e.__h = null, o = [a]), (c = l.__b) && c(e);
        try {
            t:if ("function" == typeof N) {
                if (w = e.props, S = (c = N.contextType) && r[c.__c], C = c ? S ? S.props.value : c.__ : r, n.__c ? b = (p = e.__c = n.__c).__ = p.__E : ("prototype" in N && N.prototype.render ? e.__c = p = new N(w, C) : (e.__c = p = new k(w, C), p.constructor = N, p.render = O), S && S.sub(p), p.props = w, p.state || (p.state = {}), p.context = C, p.__n = r, h = p.__d = !0, p.__h = []), null == p.__s && (p.__s = p.state), null != N.getDerivedStateFromProps && (p.__s == p.state && (p.__s = v({}, p.__s)), v(p.__s, N.getDerivedStateFromProps(w, p.__s))), f = p.props, d = p.state, h) null == N.getDerivedStateFromProps && null != p.componentWillMount && p.componentWillMount(), null != p.componentDidMount && p.__h.push(p.componentDidMount); else {
                    if (null == N.getDerivedStateFromProps && w !== f && null != p.componentWillReceiveProps && p.componentWillReceiveProps(w, C), !p.__e && null != p.shouldComponentUpdate && !1 === p.shouldComponentUpdate(w, p.__s, C) || e.__v === n.__v) {
                        p.props = w, p.state = p.__s, e.__v !== n.__v && (p.__d = !1), p.__v = e, e.__e = n.__e, e.__k = n.__k, e.__k.forEach(function (t) {
                            t && (t.__ = e)
                        }), p.__h.length && s.push(p);
                        break t
                    }
                    null != p.componentWillUpdate && p.componentWillUpdate(w, p.__s, C), null != p.componentDidUpdate && p.__h.push(function () {
                        p.componentDidUpdate(f, d, g)
                    })
                }
                p.context = C, p.props = w, p.state = p.__s, (c = l.__r) && c(e), p.__d = !1, p.__v = e, p.__P = t, c = p.render(p.props, p.state, p.context), p.state = p.__s, null != p.getChildContext && (r = v(v({}, r), p.getChildContext())), h || null == p.getSnapshotBeforeUpdate || (g = p.getSnapshotBeforeUpdate(f, d)), x = null != c && c.type === P && null == c.key ? c.props.children : c, E(t, Array.isArray(x) ? x : [x], e, n, r, i, o, s, a, u), p.base = e.__e, e.__h = null, p.__h.length && s.push(p), b && (p.__E = p.__ = null), p.__e = !1
            } else null == o && e.__v === n.__v ? (e.__k = n.__k, e.__e = n.__e) : e.__e = function (t, e, n, r, i, o, s, a) {
                var u, l, c, p, h = n.props, f = e.props, d = e.type, g = 0;
                if ("svg" === d && (i = !0), null != o) for (; g < o.length; g++) if ((u = o[g]) && (u === t || (d ? u.localName == d : 3 == u.nodeType))) {
                    t = u, o[g] = null;
                    break
                }
                if (null == t) {
                    if (null === d) return document.createTextNode(f);
                    t = i ? document.createElementNS("http://www.w3.org/2000/svg", d) : document.createElement(d, f.is && f), o = null, a = !1
                }
                if (null === d) h === f || a && t.data === f || (t.data = f); else {
                    if (o = o && m.slice.call(t.childNodes), l = (h = n.props || _).dangerouslySetInnerHTML, c = f.dangerouslySetInnerHTML, !a) {
                        if (null != o) for (h = {}, p = 0; p < t.attributes.length; p++) h[t.attributes[p].name] = t.attributes[p].value;
                        (c || l) && (c && (l && c.__html == l.__html || c.__html === t.innerHTML) || (t.innerHTML = c && c.__html || ""))
                    }
                    if (function (t, e, n, r, i) {
                        var o;
                        for (o in n) "children" === o || "key" === o || o in e || R(t, o, null, n[o], r);
                        for (o in e) i && "function" != typeof e[o] || "children" === o || "key" === o || "value" === o || "checked" === o || n[o] === e[o] || R(t, o, e[o], n[o], r)
                    }(t, f, h, i, a), c) e.__k = []; else if (g = e.props.children, E(t, Array.isArray(g) ? g : [g], e, n, r, i && "foreignObject" !== d, o, s, t.firstChild, a), null != o) for (g = o.length; g--;) null != o[g] && y(o[g]);
                    a || ("value" in f && void 0 !== (g = f.value) && (g !== t.value || "progress" === d && !g) && R(t, "value", g, h.value, !1), "checked" in f && void 0 !== (g = f.checked) && g !== t.checked && R(t, "checked", g, h.checked, !1))
                }
                return t
            }(n.__e, e, n, r, i, o, s, u);
            (c = l.diffed) && c(e)
        } catch (t) {
            e.__v = null, (u || null != o) && (e.__e = a, e.__h = !!u, o[o.indexOf(a)] = null), l.__e(t, e, n)
        }
    }

    function U(t, e) {
        l.__c && l.__c(e, t), t.some(function (e) {
            try {
                t = e.__h, e.__h = [], t.some(function (t) {
                    t.call(e)
                })
            } catch (t) {
                l.__e(t, e.__v)
            }
        })
    }

    function H(t, e, n) {
        try {
            "function" == typeof t ? t(e) : t.current = e
        } catch (t) {
            l.__e(t, n)
        }
    }

    function M(t, e, n) {
        var r, i, o;
        if (l.unmount && l.unmount(t), (r = t.ref) && (r.current && r.current !== t.__e || H(r, null, e)), n || "function" == typeof t.type || (n = null != (i = t.__e)), t.__e = t.__d = void 0, null != (r = t.__c)) {
            if (r.componentWillUnmount) try {
                r.componentWillUnmount()
            } catch (t) {
                l.__e(t, e)
            }
            r.base = r.__P = null
        }
        if (r = t.__k) for (o = 0; o < r.length; o++) r[o] && M(r[o], e, n);
        null != i && y(i)
    }

    function O(t, e, n) {
        return this.constructor(t, n)
    }

    function j(t, e, n) {
        var r, i, o;
        l.__ && l.__(t, e), i = (r = "function" == typeof n) ? null : n && n.__k || e.__k, o = [], I(e, t = (!r && n || e).__k = b(P, null, [t]), i || _, _, void 0 !== e.ownerSVGElement, !r && n ? [n] : i ? null : e.firstChild ? m.slice.call(e.childNodes) : null, o, !r && n ? n : i ? i.__e : e.firstChild, r), U(o, t)
    }

    function W() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (t) {
            var e = 16 * Math.random() | 0;
            return ("x" == t ? e : 3 & e | 8).toString(16)
        })
    }

    l = {
        __e: function (t, e) {
            for (var n, r, i; e = e.__;) if ((n = e.__c) && !n.__) try {
                if ((r = n.constructor) && null != r.getDerivedStateFromError && (n.setState(r.getDerivedStateFromError(t)), i = n.__d), null != n.componentDidCatch && (n.componentDidCatch(t), i = n.__d), i) return n.__E = n
            } catch (e) {
                t = e
            }
            throw t
        }, __v: 0
    }, c = function (t) {
        return null != t && void 0 === t.constructor
    }, k.prototype.setState = function (t, e) {
        var n;
        n = null != this.__s && this.__s !== this.state ? this.__s : this.__s = v({}, this.state), "function" == typeof t && (t = t(v({}, n), this.props)), t && v(n, t), null != t && this.__v && (e && this.__h.push(e), x(this))
    }, k.prototype.forceUpdate = function (t) {
        this.__v && (this.__e = !0, t && this.__h.push(t), x(this))
    }, k.prototype.render = P, p = [], h = "function" == typeof Promise ? Promise.prototype.then.bind(Promise.resolve()) : setTimeout, N.__r = 0, d = 0;
    var B = function () {
        function t(t) {
            this._id = void 0, this._id = t || W()
        }

        return n(t, [{
            key: "id", get: function () {
                return this._id
            }
        }]), t
    }(), z = {
        search: {placeholder: "Type a keyword..."},
        sort: {sortAsc: "Sort column ascending", sortDesc: "Sort column descending"},
        pagination: {
            previous: "Previous", next: "Next", navigate: function (t, e) {
                return "Page " + t + " of " + e
            }, page: function (t) {
                return "Page " + t
            }, showing: "Showing", of: "of", to: "to", results: "results"
        },
        loading: "Loading...",
        noRecordsFound: "No matching records found",
        error: "An error happened while fetching the data"
    }, q = function () {
        function t(t) {
            this._language = void 0, this._defaultLanguage = void 0, this._language = t, this._defaultLanguage = z
        }

        var e = t.prototype;
        return e.getString = function (t, e) {
            if (!e || !t) return null;
            var n = t.split("."), r = n[0];
            if (e[r]) {
                var i = e[r];
                return "string" == typeof i ? function () {
                    return i
                } : "function" == typeof i ? i : this.getString(n.slice(1).join("."), i)
            }
            return null
        }, e.translate = function (t) {
            var e, n = this.getString(t, this._language);
            return (e = n || this.getString(t, this._defaultLanguage)) ? e.apply(void 0, [].slice.call(arguments, 1)) : t
        }, t
    }(), G = function (t) {
        function e(e, n) {
            var r, i;
            return (r = t.call(this, e, n) || this).config = void 0, r._ = void 0, r.config = function (t) {
                if (!t) return null;
                var e = Object.keys(t);
                return e.length ? t[e[0]].props.value : null
            }(n), r.config && (r._ = (i = r.config.translator, function (t) {
                return i.translate.apply(i, [t].concat([].slice.call(arguments, 1)))
            })), r
        }

        return i(e, t), e
    }(k), X = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype.render = function () {
            return b(this.props.parentElement, {dangerouslySetInnerHTML: {__html: this.props.content}})
        }, e
    }(G);

    function $(t, e) {
        return b(X, {content: t, parentElement: e})
    }

    X.defaultProps = {parentElement: "span"};
    var K, V = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this).data = void 0, n.update(e), n
        }

        i(e, t);
        var n = e.prototype;
        return n.cast = function (t) {
            return t instanceof HTMLElement ? $(t.outerHTML) : t
        }, n.update = function (t) {
            return this.data = this.cast(t), this
        }, e
    }(B), Y = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this)._cells = void 0, n.cells = e || [], n
        }

        i(e, t);
        var r = e.prototype;
        return r.cell = function (t) {
            return this._cells[t]
        }, r.toArray = function () {
            return this.cells.map(function (t) {
                return t.data
            })
        }, e.fromCells = function (t) {
            return new e(t.map(function (t) {
                return new V(t.data)
            }))
        }, n(e, [{
            key: "cells", get: function () {
                return this._cells
            }, set: function (t) {
                this._cells = t
            }
        }, {
            key: "length", get: function () {
                return this.cells.length
            }
        }]), e
    }(B), Z = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this)._rows = void 0, n._length = void 0, n.rows = e instanceof Array ? e : e instanceof Y ? [e] : [], n
        }

        return i(e, t), e.prototype.toArray = function () {
            return this.rows.map(function (t) {
                return t.toArray()
            })
        }, e.fromRows = function (t) {
            return new e(t.map(function (t) {
                return Y.fromCells(t.cells)
            }))
        }, e.fromArray = function (t) {
            return new e((t = function (t) {
                return !t[0] || t[0] instanceof Array ? t : [t]
            }(t)).map(function (t) {
                return new Y(t.map(function (t) {
                    return new V(t)
                }))
            }))
        }, n(e, [{
            key: "rows", get: function () {
                return this._rows
            }, set: function (t) {
                this._rows = t
            }
        }, {
            key: "length", get: function () {
                return this._length || this.rows.length
            }, set: function (t) {
                this._length = t
            }
        }]), e
    }(B), J = function () {
        function t() {
            this.callbacks = void 0
        }

        var e = t.prototype;
        return e.init = function (t) {
            this.callbacks || (this.callbacks = {}), t && !this.callbacks[t] && (this.callbacks[t] = [])
        }, e.on = function (t, e) {
            return this.init(t), this.callbacks[t].push(e), this
        }, e.off = function (t, e) {
            var n = t;
            return this.init(), this.callbacks[n] && 0 !== this.callbacks[n].length ? (this.callbacks[n] = this.callbacks[n].filter(function (t) {
                return t != e
            }), this) : this
        }, e.emit = function (t) {
            var e = arguments, n = t;
            return this.init(n), this.callbacks[n].length > 0 && (this.callbacks[n].forEach(function (t) {
                return t.apply(void 0, [].slice.call(e, 1))
            }), !0)
        }, t
    }();
    !function (t) {
        t[t.Initiator = 0] = "Initiator", t[t.ServerFilter = 1] = "ServerFilter", t[t.ServerSort = 2] = "ServerSort", t[t.ServerLimit = 3] = "ServerLimit", t[t.Extractor = 4] = "Extractor", t[t.Transformer = 5] = "Transformer", t[t.Filter = 6] = "Filter", t[t.Sort = 7] = "Sort", t[t.Limit = 8] = "Limit"
    }(K || (K = {}));
    var Q = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this).id = void 0, n._props = void 0, n._props = {}, n.id = W(), e && n.setProps(e), n
        }

        i(e, t);
        var r = e.prototype;
        return r.process = function () {
            var t = [].slice.call(arguments);
            this.validateProps instanceof Function && this.validateProps.apply(this, t), this.emit.apply(this, ["beforeProcess"].concat(t));
            var e = this._process.apply(this, t);
            return this.emit.apply(this, ["afterProcess"].concat(t)), e
        }, r.setProps = function (t) {
            return Object.assign(this._props, t), this.emit("propsUpdated", this), this
        }, n(e, [{
            key: "props", get: function () {
                return this._props
            }
        }]), e
    }(J), tt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            return this.props.keyword ? (e = String(this.props.keyword).trim(), n = this.props.columns, r = this.props.ignoreHiddenColumns, i = t, o = this.props.selector, e = e.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&"), new Z(i.rows.filter(function (t, i) {
                return t.cells.some(function (t, s) {
                    if (!t) return !1;
                    if (r && n && n[s] && "object" == typeof n[s] && n[s].hidden) return !1;
                    var a = "";
                    if ("function" == typeof o) a = o(t.data, i, s); else if ("object" == typeof t.data) {
                        var u = t.data;
                        u && u.props && u.props.content && (a = u.props.content)
                    } else a = String(t.data);
                    return new RegExp(e, "gi").test(a)
                })
            }))) : t;
            var e, n, r, i, o
        }, n(e, [{
            key: "type", get: function () {
                return K.Filter
            }
        }]), e
    }(Q);

    function et() {
        var t = "gridjs";
        return "" + t + [].slice.call(arguments).reduce(function (t, e) {
            return t + "-" + e
        }, "")
    }

    function nt() {
        return [].slice.call(arguments).filter(function (t) {
            return t
        }).reduce(function (t, e) {
            return (t || "") + " " + e
        }, "").trim() || null
    }

    var rt, it = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this)._state = void 0, n.dispatcher = void 0, n.dispatcher = e, n._state = n.getInitialState(), e.register(n._handle.bind(s(n))), n
        }

        i(e, t);
        var r = e.prototype;
        return r._handle = function (t) {
            this.handle(t.type, t.payload)
        }, r.setState = function (t) {
            var e = this._state;
            this._state = t, this.emit("updated", t, e)
        }, n(e, [{
            key: "state", get: function () {
                return this._state
            }
        }]), e
    }(J), ot = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.getInitialState = function () {
            return {keyword: null}
        }, n.handle = function (t, e) {
            "SEARCH_KEYWORD" === t && this.search(e.keyword)
        }, n.search = function (t) {
            this.setState({keyword: t})
        }, e
    }(it), st = function () {
        function t(t) {
            this.dispatcher = void 0, this.dispatcher = t
        }

        return t.prototype.dispatch = function (t, e) {
            this.dispatcher.dispatch({type: t, payload: e})
        }, t
    }(), at = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype.search = function (t) {
            this.dispatch("SEARCH_KEYWORD", {keyword: t})
        }, e
    }(st), ut = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            if (!this.props.keyword) return t;
            var e = {};
            return this.props.url && (e.url = this.props.url(t.url, this.props.keyword)), this.props.body && (e.body = this.props.body(t.body, this.props.keyword)), r({}, t, e)
        }, n(e, [{
            key: "type", get: function () {
                return K.ServerFilter
            }
        }]), e
    }(Q), lt = new (function () {
        function t() {
        }

        var e = t.prototype;
        return e.format = function (t, e) {
            return "[Grid.js] [" + e.toUpperCase() + "]: " + t
        }, e.error = function (t, e) {
            void 0 === e && (e = !1);
            var n = this.format(t, "error");
            if (e) throw Error(n);
            console.error(n)
        }, e.warn = function (t) {
            console.warn(this.format(t, "warn"))
        }, e.info = function (t) {
            console.info(this.format(t, "info"))
        }, t
    }()), ct = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e
    }(G);
    t.PluginPosition = void 0, (rt = t.PluginPosition || (t.PluginPosition = {}))[rt.Header = 0] = "Header", rt[rt.Footer = 1] = "Footer", rt[rt.Cell = 2] = "Cell";
    var pt = function () {
        function t() {
            this.plugins = void 0, this.plugins = []
        }

        var e = t.prototype;
        return e.get = function (t) {
            var e = this.plugins.filter(function (e) {
                return e.id === t
            });
            return e.length > 0 ? e[0] : null
        }, e.add = function (t) {
            return t.id ? null !== this.get(t.id) ? (lt.error("Duplicate plugin ID: " + t.id), this) : (this.plugins.push(t), this) : (lt.error("Plugin ID cannot be empty"), this)
        }, e.remove = function (t) {
            return this.plugins.splice(this.plugins.indexOf(this.get(t)), 1), this
        }, e.list = function (t) {
            return (null != t || null != t ? this.plugins.filter(function (e) {
                return e.position === t
            }) : this.plugins).sort(function (t, e) {
                return t.order - e.order
            })
        }, t
    }(), ht = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype.render = function () {
            var t = this;
            if (this.props.pluginId) {
                var e = this.config.plugin.get(this.props.pluginId);
                return e ? b(P, {}, b(e.component, r({plugin: e}, e.props, this.props.props))) : null
            }
            return void 0 !== this.props.position ? b(P, {}, this.config.plugin.list(this.props.position).map(function (e) {
                return b(e.component, r({plugin: e}, e.props, t.props.props))
            })) : null
        }, e
    }(G), ft = function (t) {
        function e(e, n) {
            var r;
            (r = t.call(this, e, n) || this).searchProcessor = void 0, r.actions = void 0, r.store = void 0, r.storeUpdatedFn = void 0, r.actions = new at(r.config.dispatcher), r.store = new ot(r.config.dispatcher);
            var i, o = e.keyword;
            return e.enabled && (o && r.actions.search(o), r.storeUpdatedFn = r.storeUpdated.bind(s(r)), r.store.on("updated", r.storeUpdatedFn), i = e.server ? new ut({
                keyword: e.keyword,
                url: e.server.url,
                body: e.server.body
            }) : new tt({
                keyword: e.keyword,
                columns: r.config.header && r.config.header.columns,
                ignoreHiddenColumns: e.ignoreHiddenColumns || void 0 === e.ignoreHiddenColumns,
                selector: e.selector
            }), r.searchProcessor = i, r.config.pipeline.register(i)), r
        }

        i(e, t);
        var n = e.prototype;
        return n.componentWillUnmount = function () {
            this.config.pipeline.unregister(this.searchProcessor), this.store.off("updated", this.storeUpdatedFn)
        }, n.storeUpdated = function (t) {
            this.searchProcessor.setProps({keyword: t.keyword})
        }, n.onChange = function (t) {
            this.actions.search(t.target.value)
        }, n.render = function () {
            if (!this.props.enabled) return null;
            var t, e, n, r = this.onChange.bind(this);
            return this.searchProcessor instanceof ut && (t = r, e = this.props.debounceTimeout, r = function () {
                var r = arguments;
                return new Promise(function (i) {
                    n && clearTimeout(n), n = setTimeout(function () {
                        return i(t.apply(void 0, [].slice.call(r)))
                    }, e)
                })
            }), b("div", {className: et(nt("search", this.config.className.search))}, b("input", {
                type: "search",
                placeholder: this._("search.placeholder"),
                "aria-label": this._("search.placeholder"),
                onInput: r,
                className: nt(et("input"), et("search", "input")),
                value: this.store.state.keyword
            }))
        }, e
    }(ct);
    ft.defaultProps = {debounceTimeout: 250};
    var dt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var r = e.prototype;
        return r.validateProps = function () {
            if (isNaN(Number(this.props.limit)) || isNaN(Number(this.props.page))) throw Error("Invalid parameters passed")
        }, r._process = function (t) {
            var e = this.props.page;
            return new Z(t.rows.slice(e * this.props.limit, (e + 1) * this.props.limit))
        }, n(e, [{
            key: "type", get: function () {
                return K.Limit
            }
        }]), e
    }(Q), _t = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            var e = {};
            return this.props.url && (e.url = this.props.url(t.url, this.props.page, this.props.limit)), this.props.body && (e.body = this.props.body(t.body, this.props.page, this.props.limit)), r({}, t, e)
        }, n(e, [{
            key: "type", get: function () {
                return K.ServerLimit
            }
        }]), e
    }(Q), mt = function (t) {
        function e(e, n) {
            var r;
            return (r = t.call(this, e, n) || this).processor = void 0, r.onUpdateFn = void 0, r.setTotalFromTabularFn = void 0, r.state = {
                limit: e.limit,
                page: e.page || 0,
                total: 0
            }, r
        }

        i(e, t);
        var r = e.prototype;
        return r.componentWillMount = function () {
            var t, e = this;
            this.props.enabled && (this.setTotalFromTabularFn = this.setTotalFromTabular.bind(this), this.props.server ? (t = new _t({
                limit: this.state.limit,
                page: this.state.page,
                url: this.props.server.url,
                body: this.props.server.body
            }), this.config.pipeline.on("afterProcess", this.setTotalFromTabularFn)) : (t = new dt({
                limit: this.state.limit,
                page: this.state.page
            })).on("beforeProcess", this.setTotalFromTabularFn), this.processor = t, this.config.pipeline.register(t), this.config.pipeline.on("error", function () {
                e.setState({total: 0, page: 0})
            }))
        }, r.setTotalFromTabular = function (t) {
            this.setTotal(t.length)
        }, r.onUpdate = function (t) {
            this.props.resetPageOnUpdate && t !== this.processor && this.setPage(0)
        }, r.componentDidMount = function () {
            this.onUpdateFn = this.onUpdate.bind(this), this.config.pipeline.on("updated", this.onUpdateFn)
        }, r.componentWillUnmount = function () {
            this.config.pipeline.unregister(this.processor), this.config.pipeline.off("updated", this.onUpdateFn)
        }, r.setPage = function (t) {
            if (t >= this.pages || t < 0 || t === this.state.page) return null;
            this.setState({page: t}), this.processor.setProps({page: t})
        }, r.setTotal = function (t) {
            this.setState({total: t})
        }, r.renderPages = function () {
            var t = this;
            if (this.props.buttonsCount <= 0) return null;
            var e = Math.min(this.pages, this.props.buttonsCount), n = Math.min(this.state.page, Math.floor(e / 2));
            return this.state.page + Math.floor(e / 2) >= this.pages && (n = e - (this.pages - this.state.page)), b(P, null, this.pages > e && this.state.page - n > 0 && b(P, null, b("button", {
                tabIndex: 0,
                role: "button",
                onClick: this.setPage.bind(this, 0),
                title: this._("pagination.firstPage"),
                "aria-label": this._("pagination.firstPage"),
                className: this.config.className.paginationButton
            }, this._("1")), b("button", {
                tabIndex: -1,
                className: nt(et("spread"), this.config.className.paginationButton)
            }, "...")), Array.from(Array(e).keys()).map(function (e) {
                return t.state.page + (e - n)
            }).map(function (e) {
                return b("button", {
                    tabIndex: 0,
                    role: "button",
                    onClick: t.setPage.bind(t, e),
                    className: nt(t.state.page === e ? nt(et("currentPage"), t.config.className.paginationButtonCurrent) : null, t.config.className.paginationButton),
                    title: t._("pagination.page", e + 1),
                    "aria-label": t._("pagination.page", e + 1)
                }, t._("" + (e + 1)))
            }), this.pages > e && this.pages > this.state.page + n + 1 && b(P, null, b("button", {
                tabIndex: -1,
                className: nt(et("spread"), this.config.className.paginationButton)
            }, "..."), b("button", {
                tabIndex: 0,
                role: "button",
                onClick: this.setPage.bind(this, this.pages - 1),
                title: this._("pagination.page", this.pages),
                "aria-label": this._("pagination.page", this.pages),
                className: this.config.className.paginationButton
            }, this._("" + this.pages))))
        }, r.renderSummary = function () {
            return b(P, null, this.props.summary && this.state.total > 0 && b("div", {
                role: "status",
                "aria-live": "polite",
                className: nt(et("summary"), this.config.className.paginationSummary),
                title: this._("pagination.navigate", this.state.page + 1, this.pages)
            }, this._("pagination.showing"), " ", b("b", null, this._("" + (this.state.page * this.state.limit + 1))), " ", this._("pagination.to"), " ", b("b", null, this._("" + Math.min((this.state.page + 1) * this.state.limit, this.state.total))), " ", this._("pagination.of"), " ", b("b", null, this._("" + this.state.total)), " ", this._("pagination.results")))
        }, r.render = function () {
            return this.props.enabled ? b("div", {className: nt(et("pagination"), this.config.className.pagination)}, this.renderSummary(), b("div", {className: et("pages")}, this.props.prevButton && b("button", {
                tabIndex: 0,
                role: "button",
                disabled: 0 === this.state.page,
                onClick: this.setPage.bind(this, this.state.page - 1),
                title: this._("pagination.previous"),
                "aria-label": this._("pagination.previous"),
                className: nt(this.config.className.paginationButton, this.config.className.paginationButtonPrev)
            }, this._("pagination.previous")), this.renderPages(), this.props.nextButton && b("button", {
                tabIndex: 0,
                role: "button",
                disabled: this.pages === this.state.page + 1 || 0 === this.pages,
                onClick: this.setPage.bind(this, this.state.page + 1),
                title: this._("pagination.next"),
                "aria-label": this._("pagination.next"),
                className: nt(this.config.className.paginationButton, this.config.className.paginationButtonNext)
            }, this._("pagination.next")))) : null
        }, n(e, [{
            key: "pages", get: function () {
                return Math.ceil(this.state.total / this.state.limit)
            }
        }]), e
    }(ct);

    function gt(t, e) {
        return "string" == typeof t ? t.indexOf("%") > -1 ? e / 100 * parseInt(t, 10) : parseInt(t, 10) : t
    }

    function vt(t) {
        return t ? Math.floor(t) + "px" : ""
    }

    mt.defaultProps = {summary: !0, nextButton: !0, prevButton: !0, buttonsCount: 3, limit: 10, resetPageOnUpdate: !0};
    var yt = function (t) {
        function e(e, n) {
            var r;
            return (r = t.call(this, e, n) || this).tableElement = void 0, r.tableClassName = void 0, r.tableStyle = void 0, r.tableElement = r.props.tableRef.current.base.cloneNode(!0), r.tableElement.style.position = "absolute", r.tableElement.style.width = "100%", r.tableElement.style.zIndex = "-2147483640", r.tableElement.style.visibility = "hidden", r.tableClassName = r.tableElement.className, r.tableStyle = r.tableElement.style.cssText, r
        }

        i(e, t);
        var n = e.prototype;
        return n.widths = function () {
            this.tableElement.className = this.tableClassName + " " + et("shadowTable"), this.tableElement.style.tableLayout = "auto", this.tableElement.style.width = "auto", this.tableElement.style.padding = "0", this.tableElement.style.margin = "0", this.tableElement.style.border = "none", this.tableElement.style.outline = "none";
            var t = Array.from(this.base.parentNode.querySelectorAll("thead th")).reduce(function (t, e) {
                var n;
                return e.style.width = e.clientWidth + "px", r(((n = {})[e.getAttribute("data-column-id")] = {minWidth: e.clientWidth}, n), t)
            }, {});
            return this.tableElement.className = this.tableClassName, this.tableElement.style.cssText = this.tableStyle, this.tableElement.style.tableLayout = "auto", Array.from(this.base.parentNode.querySelectorAll("thead th")).reduce(function (t, e) {
                return t[e.getAttribute("data-column-id")].width = e.clientWidth, t
            }, t)
        }, n.render = function () {
            var t = this;
            return this.props.tableRef.current ? b("div", {
                ref: function (e) {
                    e && e.appendChild(t.tableElement)
                }
            }) : null
        }, e
    }(G);

    function bt(t) {
        if (!t) return "";
        var e = t.split(" ");
        return 1 === e.length && /([a-z][A-Z])+/g.test(t) ? t : e.map(function (t, e) {
            return 0 == e ? t.toLowerCase() : t.charAt(0).toUpperCase() + t.slice(1).toLowerCase()
        }).join("")
    }

    var wt = function (e) {
            function o() {
                var t;
                return (t = e.call(this) || this)._columns = void 0, t._columns = [], t
            }

            i(o, e);
            var s = o.prototype;
            return s.adjustWidth = function (t) {
                var e = t.container, n = t.tableRef, r = t.tempRef, i = t.tempRef || !0;
                if (!e) return this;
                var s = e.clientWidth, a = {current: null}, l = {};
                if (n.current && i) {
                    var c = b(yt, {tableRef: n});
                    c.ref = a, j(c, r.current), l = a.current.widths()
                }
                for (var p, h = u(o.tabularFormat(this.columns).reduce(function (t, e) {
                    return t.concat(e)
                }, [])); !(p = h()).done;) {
                    var f = p.value;
                    f.columns && f.columns.length > 0 || (!f.width && i ? f.id in l && (f.width = vt(l[f.id].width), f.minWidth = vt(l[f.id].minWidth)) : f.width = vt(gt(f.width, s)))
                }
                return n.current && i && j(null, r.current), this
            }, s.setSort = function (t, e) {
                for (var n, i = u(e || this.columns || []); !(n = i()).done;) {
                    var o = n.value;
                    o.columns && o.columns.length > 0 && (o.sort = {enabled: !1}), void 0 === o.sort && t.sort && (o.sort = {enabled: !0}), o.sort ? "object" == typeof o.sort && (o.sort = r({enabled: !0}, o.sort)) : o.sort = {enabled: !1}, o.columns && this.setSort(t, o.columns)
                }
            }, s.setFixedHeader = function (t, e) {
                for (var n, r = u(e || this.columns || []); !(n = r()).done;) {
                    var i = n.value;
                    void 0 === i.fixedHeader && (i.fixedHeader = t.fixedHeader), i.columns && this.setFixedHeader(t, i.columns)
                }
            }, s.setResizable = function (t, e) {
                for (var n, r = u(e || this.columns || []); !(n = r()).done;) {
                    var i = n.value;
                    void 0 === i.resizable && (i.resizable = t.resizable), i.columns && this.setResizable(t, i.columns)
                }
            }, s.setID = function (t) {
                for (var e, n = u(t || this.columns || []); !(e = n()).done;) {
                    var r = e.value;
                    r.id || "string" != typeof r.name || (r.id = bt(r.name)), r.id || lt.error('Could not find a valid ID for one of the columns. Make sure a valid "id" is set for all columns.'), r.columns && this.setID(r.columns)
                }
            }, s.populatePlugins = function (e, n) {
                for (var i, o = u(n); !(i = o()).done;) {
                    var s = i.value;
                    void 0 !== s.plugin && e.plugin.add(r({
                        id: s.id,
                        props: {}
                    }, s.plugin, {position: t.PluginPosition.Cell}))
                }
            }, o.fromColumns = function (t) {
                for (var e, n = new o, r = u(t); !(e = r()).done;) {
                    var i = e.value;
                    if ("string" == typeof i || c(i)) n.columns.push({name: i}); else if ("object" == typeof i) {
                        var s = i;
                        s.columns && (s.columns = o.fromColumns(s.columns).columns), "object" == typeof s.plugin && void 0 === s.data && (s.data = null), n.columns.push(i)
                    }
                }
                return n
            }, o.fromUserConfig = function (t) {
                var e = new o;
                return t.from ? e.columns = o.fromHTMLTable(t.from).columns : t.columns ? e.columns = o.fromColumns(t.columns).columns : !t.data || "object" != typeof t.data[0] || t.data[0] instanceof Array || (e.columns = Object.keys(t.data[0]).map(function (t) {
                    return {name: t}
                })), e.columns.length ? (e.setID(), e.setSort(t), e.setFixedHeader(t), e.setResizable(t), e.populatePlugins(t, e.columns), e) : null
            }, o.fromHTMLTable = function (t) {
                for (var e, n = new o, r = u(t.querySelector("thead").querySelectorAll("th")); !(e = r()).done;) {
                    var i = e.value;
                    n.columns.push({name: i.innerHTML, width: i.width})
                }
                return n
            }, o.tabularFormat = function (t) {
                var e = [], n = t || [], r = [];
                if (n && n.length) {
                    e.push(n);
                    for (var i, o = u(n); !(i = o()).done;) {
                        var s = i.value;
                        s.columns && s.columns.length && (r = r.concat(s.columns))
                    }
                    r.length && (e = e.concat(this.tabularFormat(r)))
                }
                return e
            }, o.leafColumns = function (t) {
                var e = [], n = t || [];
                if (n && n.length) for (var r, i = u(n); !(r = i()).done;) {
                    var o = r.value;
                    o.columns && 0 !== o.columns.length || e.push(o), o.columns && (e = e.concat(this.leafColumns(o.columns)))
                }
                return e
            }, o.maximumDepth = function (t) {
                return this.tabularFormat([t]).length - 1
            }, n(o, [{
                key: "columns", get: function () {
                    return this._columns
                }, set: function (t) {
                    this._columns = t
                }
            }, {
                key: "visibleColumns", get: function () {
                    return this._columns.filter(function (t) {
                        return !t.hidden
                    })
                }
            }]), o
        }(B), Pt = function () {
            function t() {
                this._callbacks = void 0, this._isDispatching = void 0, this._isHandled = void 0, this._isPending = void 0, this._lastID = void 0, this._pendingPayload = void 0, this._callbacks = {}, this._isDispatching = !1, this._isHandled = {}, this._isPending = {}, this._lastID = 1
            }

            var e = t.prototype;
            return e.register = function (t) {
                var e = "ID_" + this._lastID++;
                return this._callbacks[e] = t, e
            }, e.unregister = function (t) {
                if (!this._callbacks[t]) throw Error("Dispatcher.unregister(...): " + t + " does not map to a registered callback.");
                delete this._callbacks[t]
            }, e.waitFor = function (t) {
                if (!this._isDispatching) throw Error("Dispatcher.waitFor(...): Must be invoked while dispatching.");
                for (var e = 0; e < t.length; e++) {
                    var n = t[e];
                    if (this._isPending[n]) {
                        if (!this._isHandled[n]) throw Error("Dispatcher.waitFor(...): Circular dependency detected while ' +\n            'waiting for " + n + ".")
                    } else {
                        if (!this._callbacks[n]) throw Error("Dispatcher.waitFor(...): " + n + " does not map to a registered callback.");
                        this._invokeCallback(n)
                    }
                }
            }, e.dispatch = function (t) {
                if (this._isDispatching) throw Error("Dispatch.dispatch(...): Cannot dispatch in the middle of a dispatch.");
                this._startDispatching(t);
                try {
                    for (var e in this._callbacks) this._isPending[e] || this._invokeCallback(e)
                } finally {
                    this._stopDispatching()
                }
            }, e.isDispatching = function () {
                return this._isDispatching
            }, e._invokeCallback = function (t) {
                this._isPending[t] = !0, this._callbacks[t](this._pendingPayload), this._isHandled[t] = !0
            }, e._startDispatching = function (t) {
                for (var e in this._callbacks) this._isPending[e] = !1, this._isHandled[e] = !1;
                this._pendingPayload = t, this._isDispatching = !0
            }, e._stopDispatching = function () {
                delete this._pendingPayload, this._isDispatching = !1
            }, t
        }(), kt = function () {
        }, St = function (t) {
            function e(e) {
                var n;
                return (n = t.call(this) || this).data = void 0, n.set(e), n
            }

            i(e, t);
            var n = e.prototype;
            return n.get = function () {
                try {
                    return Promise.resolve(this.data()).then(function (t) {
                        return {data: t, total: t.length}
                    })
                } catch (t) {
                    return Promise.reject(t)
                }
            }, n.set = function (t) {
                return t instanceof Array ? this.data = function () {
                    return t
                } : t instanceof Function && (this.data = t), this
            }, e
        }(kt), Ct = function (t) {
            function e(e) {
                var n;
                return (n = t.call(this) || this).options = void 0, n.options = e, n
            }

            i(e, t);
            var n = e.prototype;
            return n.handler = function (t) {
                return "function" == typeof this.options.handle ? this.options.handle(t) : t.ok ? t.json() : (lt.error("Could not fetch data: " + t.status + " - " + t.statusText, !0), null)
            }, n.get = function (t) {
                var e = r({}, this.options, t);
                return "function" == typeof e.data ? e.data(e) : fetch(e.url, e).then(this.handler.bind(this)).then(function (t) {
                    return {data: e.then(t), total: "function" == typeof e.total ? e.total(t) : void 0}
                })
            }, e
        }(kt), xt = function () {
            function t() {
            }

            return t.createFromUserConfig = function (t) {
                var e = null;
                return t.data && (e = new St(t.data)), t.from && (e = new St(this.tableElementToArray(t.from)), t.from.style.display = "none"), t.server && (e = new Ct(t.server)), e || lt.error("Could not determine the storage type", !0), e
            }, t.tableElementToArray = function (t) {
                for (var e, n, r = [], i = u(t.querySelector("tbody").querySelectorAll("tr")); !(e = i()).done;) {
                    for (var o, s = [], a = u(e.value.querySelectorAll("td")); !(o = a()).done;) {
                        var l = o.value;
                        1 === l.childNodes.length && l.childNodes[0].nodeType === Node.TEXT_NODE ? s.push((n = l.innerHTML, (new DOMParser).parseFromString(n, "text/html").documentElement.textContent)) : s.push($(l.innerHTML))
                    }
                    r.push(s)
                }
                return r
            }, t
        }(),
        Nt = "undefined" != typeof Symbol ? Symbol.iterator || (Symbol.iterator = Symbol("Symbol.iterator")) : "@@iterator";

    function Et(t, e, n) {
        if (!t.s) {
            if (n instanceof Ft) {
                if (!n.s) return void (n.o = Et.bind(null, t, e));
                1 & e && (e = n.s), n = n.v
            }
            if (n && n.then) return void n.then(Et.bind(null, t, e), Et.bind(null, t, 2));
            t.s = e, t.v = n;
            var r = t.o;
            r && r(t)
        }
    }

    var Ft = function () {
        function t() {
        }

        return t.prototype.then = function (e, n) {
            var r = new t, i = this.s;
            if (i) {
                var o = 1 & i ? e : n;
                if (o) {
                    try {
                        Et(r, 1, o(this.v))
                    } catch (t) {
                        Et(r, 2, t)
                    }
                    return r
                }
                return this
            }
            return this.o = function (t) {
                try {
                    var i = t.v;
                    1 & t.s ? Et(r, 1, e ? e(i) : i) : n ? Et(r, 1, n(i)) : Et(r, 2, i)
                } catch (t) {
                    Et(r, 2, t)
                }
            }, r
        }, t
    }();

    function Tt(t) {
        return t instanceof Ft && 1 & t.s
    }

    var Dt, Rt = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this)._steps = new Map, n.cache = new Map, n.lastProcessorIndexUpdated = -1, e && e.forEach(function (t) {
                return n.register(t)
            }), n
        }

        i(e, t);
        var r = e.prototype;
        return r.clearCache = function () {
            this.cache = new Map, this.lastProcessorIndexUpdated = -1
        }, r.register = function (t, e) {
            if (void 0 === e && (e = null), null === t.type) throw Error("Processor type is not defined");
            t.on("propsUpdated", this.processorPropsUpdated.bind(this)), this.addProcessorByPriority(t, e), this.afterRegistered(t)
        }, r.unregister = function (t) {
            if (t) {
                var e = this._steps.get(t.type);
                e && e.length && (this._steps.set(t.type, e.filter(function (e) {
                    return e != t
                })), this.emit("updated", t))
            }
        }, r.addProcessorByPriority = function (t, e) {
            var n = this._steps.get(t.type);
            if (!n) {
                var r = [];
                this._steps.set(t.type, r), n = r
            }
            if (null === e || e < 0) n.push(t); else if (n[e]) {
                var i = n.slice(0, e - 1), o = n.slice(e + 1);
                this._steps.set(t.type, i.concat(t).concat(o))
            } else n[e] = t
        }, r.getStepsByType = function (t) {
            return this.steps.filter(function (e) {
                return e.type === t
            })
        }, r.getSortedProcessorTypes = function () {
            return Object.keys(K).filter(function (t) {
                return !isNaN(Number(t))
            }).map(function (t) {
                return Number(t)
            })
        }, r.process = function (t) {
            try {
                var e = this, n = function (t) {
                    return e.lastProcessorIndexUpdated = i.length, e.emit("afterProcess", o), o
                }, r = e.lastProcessorIndexUpdated, i = e.steps, o = t, s = function (t, n) {
                    try {
                        var s = function (t, e, n) {
                            if ("function" == typeof t[Nt]) {
                                var r, i, o, s = t[Nt]();
                                if (function t(n) {
                                    try {
                                        for (; !(r = s.next()).done;) if ((n = e(r.value)) && n.then) {
                                            if (!Tt(n)) return void n.then(t, o || (o = Et.bind(null, i = new Ft, 2)));
                                            n = n.v
                                        }
                                        i ? Et(i, 1, n) : i = n
                                    } catch (t) {
                                        Et(i || (i = new Ft), 2, t)
                                    }
                                }(), s.return) {
                                    var a = function (t) {
                                        try {
                                            r.done || s.return()
                                        } catch (t) {
                                        }
                                        return t
                                    };
                                    if (i && i.then) return i.then(a, function (t) {
                                        throw a(t)
                                    });
                                    a()
                                }
                                return i
                            }
                            if (!("length" in t)) throw new TypeError("Object is not iterable");
                            for (var u = [], l = 0; l < t.length; l++) u.push(t[l]);
                            return function (t, e, n) {
                                var r, i, o = -1;
                                return function n(s) {
                                    try {
                                        for (; ++o < t.length;) if ((s = e(o)) && s.then) {
                                            if (!Tt(s)) return void s.then(n, i || (i = Et.bind(null, r = new Ft, 2)));
                                            s = s.v
                                        }
                                        r ? Et(r, 1, s) : r = s
                                    } catch (t) {
                                        Et(r || (r = new Ft), 2, t)
                                    }
                                }(), r
                            }(u, function (t) {
                                return e(u[t])
                            })
                        }(i, function (t) {
                            var n = e.findProcessorIndexByID(t.id), i = function () {
                                if (n >= r) return Promise.resolve(t.process(o)).then(function (n) {
                                    e.cache.set(t.id, o = n)
                                });
                                o = e.cache.get(t.id)
                            }();
                            if (i && i.then) return i.then(function () {
                            })
                        })
                    } catch (t) {
                        return n(t)
                    }
                    return s && s.then ? s.then(void 0, n) : s
                }(0, function (t) {
                    throw lt.error(t), e.emit("error", o), t
                });
                return Promise.resolve(s && s.then ? s.then(n) : n())
            } catch (t) {
                return Promise.reject(t)
            }
        }, r.findProcessorIndexByID = function (t) {
            return this.steps.findIndex(function (e) {
                return e.id == t
            })
        }, r.setLastProcessorIndex = function (t) {
            var e = this.findProcessorIndexByID(t.id);
            this.lastProcessorIndexUpdated > e && (this.lastProcessorIndexUpdated = e)
        }, r.processorPropsUpdated = function (t) {
            this.setLastProcessorIndex(t), this.emit("propsUpdated"), this.emit("updated", t)
        }, r.afterRegistered = function (t) {
            this.setLastProcessorIndex(t), this.emit("afterRegister"), this.emit("updated", t)
        }, n(e, [{
            key: "steps", get: function () {
                for (var t, e = [], n = u(this.getSortedProcessorTypes()); !(t = n()).done;) {
                    var r = this._steps.get(t.value);
                    r && r.length && (e = e.concat(r))
                }
                return e.filter(function (t) {
                    return t
                })
            }
        }]), e
    }(J), Lt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            try {
                return Promise.resolve(this.props.storage.get(t))
            } catch (t) {
                return Promise.reject(t)
            }
        }, n(e, [{
            key: "type", get: function () {
                return K.Extractor
            }
        }]), e
    }(Q), At = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            var e = Z.fromArray(t.data);
            return e.length = t.total, e
        }, n(e, [{
            key: "type", get: function () {
                return K.Transformer
            }
        }]), e
    }(Q), It = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function () {
            return Object.entries(this.props.serverStorageOptions).filter(function (t) {
                return "function" != typeof t[1]
            }).reduce(function (t, e) {
                var n;
                return r({}, t, ((n = {})[e[0]] = e[1], n))
            }, {})
        }, n(e, [{
            key: "type", get: function () {
                return K.Initiator
            }
        }]), e
    }(Q), Ut = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var r = e.prototype;
        return r.castData = function (t) {
            if (!t || !t.length) return [];
            if (!this.props.header || !this.props.header.columns) return t;
            var e = wt.leafColumns(this.props.header.columns);
            return t[0] instanceof Array ? t.map(function (t) {
                var n = 0;
                return e.map(function (e, r) {
                    return void 0 !== e.data ? (n++, "function" == typeof e.data ? e.data(t) : e.data) : t[r - n]
                })
            }) : "object" != typeof t[0] || t[0] instanceof Array ? [] : t.map(function (t) {
                return e.map(function (e, n) {
                    return void 0 !== e.data ? "function" == typeof e.data ? e.data(t) : e.data : e.id ? t[e.id] : (lt.error("Could not find the correct cell for column at position " + n + ".\n                          Make sure either 'id' or 'selector' is defined for all columns."), null)
                })
            })
        }, r._process = function (t) {
            return {data: this.castData(t.data), total: t.total}
        }, n(e, [{
            key: "type", get: function () {
                return K.Transformer
            }
        }]), e
    }(Q), Ht = function () {
        function t() {
        }

        return t.createFromConfig = function (t) {
            var e = new Rt;
            return t.storage instanceof Ct && e.register(new It({serverStorageOptions: t.server})), e.register(new Lt({storage: t.storage})), e.register(new Ut({header: t.header})), e.register(new At), e
        }, t
    }(), Mt = function () {
        function e(t) {
            this._userConfig = void 0, Object.assign(this, r({}, e.defaultConfig(), t)), this._userConfig = {}
        }

        var n = e.prototype;
        return n.assign = function (t) {
            for (var e = 0, n = Object.keys(t); e < n.length; e++) {
                var r = n[e];
                "_userConfig" !== r && (this[r] = t[r])
            }
            return this
        }, n.update = function (t) {
            return t ? (this._userConfig = r({}, this._userConfig, t), this.assign(e.fromUserConfig(this._userConfig)), this) : this
        }, e.defaultConfig = function () {
            return {
                plugin: new pt,
                dispatcher: new Pt,
                tableRef: {current: null},
                tempRef: {current: null},
                width: "100%",
                height: "auto",
                autoWidth: !0,
                style: {},
                className: {}
            }
        }, e.fromUserConfig = function (n) {
            var i = new e(n);
            return i._userConfig = n, "boolean" == typeof n.sort && n.sort && i.assign({sort: {multiColumn: !0}}), i.assign({header: wt.fromUserConfig(i)}), i.assign({storage: xt.createFromUserConfig(n)}), i.assign({pipeline: Ht.createFromConfig(i)}), i.assign({translator: new q(n.language)}), i.plugin.add({
                id: "search",
                position: t.PluginPosition.Header,
                component: ft,
                props: r({enabled: !0 === n.search || n.search instanceof Object}, n.search)
            }), i.plugin.add({
                id: "pagination",
                position: t.PluginPosition.Footer,
                component: mt,
                props: r({enabled: !0 === n.pagination || n.pagination instanceof Object}, n.pagination)
            }), n.plugins && n.plugins.forEach(function (t) {
                return i.plugin.add(t)
            }), i
        }, e
    }();
    !function (t) {
        t[t.Init = 0] = "Init", t[t.Loading = 1] = "Loading", t[t.Loaded = 2] = "Loaded", t[t.Rendered = 3] = "Rendered", t[t.Error = 4] = "Error"
    }(Dt || (Dt = {}));
    var Ot, jt, Wt, Bt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.content = function () {
            return this.props.column && "function" == typeof this.props.column.formatter ? this.props.column.formatter(this.props.cell.data, this.props.row, this.props.column) : this.props.column && this.props.column.plugin ? b(ht, {
                pluginId: this.props.column.id,
                props: {column: this.props.column, cell: this.props.cell, row: this.props.row}
            }) : this.props.cell.data
        }, n.handleClick = function (t) {
            this.props.messageCell || this.config.eventEmitter.emit("cellClick", t, this.props.cell, this.props.column, this.props.row)
        }, n.getCustomAttributes = function (t) {
            return t ? "function" == typeof t.attributes ? t.attributes(this.props.cell.data, this.props.row, this.props.column) : t.attributes : {}
        }, n.render = function () {
            return b("td", r({
                role: this.props.role,
                colSpan: this.props.colSpan,
                "data-column-id": this.props.column && this.props.column.id,
                className: nt(et("td"), this.props.className, this.config.className.td),
                style: r({}, this.props.style, this.config.style.td),
                onClick: this.handleClick.bind(this)
            }, this.getCustomAttributes(this.props.column)), this.content())
        }, e
    }(G), zt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.getColumn = function (t) {
            if (this.props.header) {
                var e = wt.leafColumns(this.props.header.columns);
                if (e) return e[t]
            }
            return null
        }, n.handleClick = function (t) {
            this.props.messageRow || this.config.eventEmitter.emit("rowClick", t, this.props.row)
        }, n.getChildren = function () {
            var t = this;
            return this.props.children ? this.props.children : b(P, null, this.props.row.cells.map(function (e, n) {
                var r = t.getColumn(n);
                return r && r.hidden ? null : b(Bt, {key: e.id, cell: e, row: t.props.row, column: r})
            }))
        }, n.render = function () {
            return b("tr", {
                className: nt(et("tr"), this.config.className.tr),
                onClick: this.handleClick.bind(this)
            }, this.getChildren())
        }, e
    }(G), qt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype.render = function () {
            return b(zt, {messageRow: !0}, b(Bt, {
                role: "alert",
                colSpan: this.props.colSpan,
                messageCell: !0,
                cell: new V(this.props.message),
                className: nt(et("message"), this.props.className ? this.props.className : null)
            }))
        }, e
    }(G), Gt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.headerLength = function () {
            return this.props.header ? this.props.header.visibleColumns.length : 0
        }, n.render = function () {
            var t = this;
            return b("tbody", {className: nt(et("tbody"), this.config.className.tbody)}, this.props.data && this.props.data.rows.map(function (e) {
                return b(zt, {key: e.id, row: e, header: t.props.header})
            }), this.props.status === Dt.Loading && (!this.props.data || 0 === this.props.data.length) && b(qt, {
                message: this._("loading"),
                colSpan: this.headerLength(),
                className: nt(et("loading"), this.config.className.loading)
            }), this.props.status === Dt.Rendered && this.props.data && 0 === this.props.data.length && b(qt, {
                message: this._("noRecordsFound"),
                colSpan: this.headerLength(),
                className: nt(et("notfound"), this.config.className.notfound)
            }), this.props.status === Dt.Error && b(qt, {
                message: this._("error"),
                colSpan: this.headerLength(),
                className: nt(et("error"), this.config.className.error)
            }))
        }, e
    }(G), Xt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var r = e.prototype;
        return r.validateProps = function () {
            for (var t, e = u(this.props.columns); !(t = e()).done;) {
                var n = t.value;
                void 0 === n.direction && (n.direction = 1), 1 !== n.direction && -1 !== n.direction && lt.error("Invalid sort direction " + n.direction)
            }
        }, r.compare = function (t, e) {
            return t > e ? 1 : t < e ? -1 : 0
        }, r.compareWrapper = function (t, e) {
            for (var n, r = 0, i = u(this.props.columns); !(n = i()).done;) {
                var o = n.value;
                if (0 !== r) break;
                var s = t.cells[o.index].data, a = e.cells[o.index].data;
                r |= "function" == typeof o.compare ? o.compare(s, a) * o.direction : this.compare(s, a) * o.direction
            }
            return r
        }, r._process = function (t) {
            var e = [].concat(t.rows);
            e.sort(this.compareWrapper.bind(this));
            var n = new Z(e);
            return n.length = t.length, n
        }, n(e, [{
            key: "type", get: function () {
                return K.Sort
            }
        }]), e
    }(Q), $t = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.getInitialState = function () {
            return []
        }, n.handle = function (t, e) {
            "SORT_COLUMN" === t ? this.sortColumn(e.index, e.direction, e.multi, e.compare) : "SORT_COLUMN_TOGGLE" === t && this.sortToggle(e.index, e.multi, e.compare)
        }, n.sortToggle = function (t, e, n) {
            var r = [].concat(this.state).find(function (e) {
                return e.index === t
            });
            this.sortColumn(t, r && 1 === r.direction ? -1 : 1, e, n)
        }, n.sortColumn = function (t, e, n, r) {
            var i = [].concat(this.state), o = i.length, s = i.find(function (e) {
                return e.index === t
            }), a = !1, u = !1, l = !1, c = !1;
            if (void 0 !== s ? n ? -1 === s.direction ? l = !0 : c = !0 : 1 === o ? c = !0 : o > 1 && (u = !0, a = !0) : 0 === o ? a = !0 : o > 0 && !n ? (a = !0, u = !0) : o > 0 && n && (a = !0), u && (i = []), a) i.push({
                index: t,
                direction: e,
                compare: r
            }); else if (c) {
                var p = i.indexOf(s);
                i[p].direction = e
            } else if (l) {
                var h = i.indexOf(s);
                i.splice(h, 1)
            }
            this.setState(i)
        }, e
    }(it), Kt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.sortColumn = function (t, e, n, r) {
            this.dispatch("SORT_COLUMN", {index: t, direction: e, multi: n, compare: r})
        }, n.sortToggle = function (t, e, n) {
            this.dispatch("SORT_COLUMN_TOGGLE", {index: t, multi: e, compare: n})
        }, e
    }(st), Vt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype._process = function (t) {
            var e = {};
            return this.props.url && (e.url = this.props.url(t.url, this.props.columns)), this.props.body && (e.body = this.props.body(t.body, this.props.columns)), r({}, t, e)
        }, n(e, [{
            key: "type", get: function () {
                return K.ServerSort
            }
        }]), e
    }(Q), Yt = function (t) {
        function e(e, n) {
            var r;
            return (r = t.call(this, e, n) || this).sortProcessor = void 0, r.actions = void 0, r.store = void 0, r.updateStateFn = void 0, r.updateSortProcessorFn = void 0, r.actions = new Kt(r.config.dispatcher), r.store = new $t(r.config.dispatcher), e.enabled && (r.sortProcessor = r.getOrCreateSortProcessor(), r.updateStateFn = r.updateState.bind(s(r)), r.store.on("updated", r.updateStateFn), r.state = {direction: 0}), r
        }

        i(e, t);
        var n = e.prototype;
        return n.componentWillUnmount = function () {
            this.config.pipeline.unregister(this.sortProcessor), this.store.off("updated", this.updateStateFn), this.updateSortProcessorFn && this.store.off("updated", this.updateSortProcessorFn)
        }, n.updateState = function () {
            var t = this, e = this.store.state.find(function (e) {
                return e.index === t.props.index
            });
            this.setState(e ? {direction: e.direction} : {direction: 0})
        }, n.updateSortProcessor = function (t) {
            this.sortProcessor.setProps({columns: t})
        }, n.getOrCreateSortProcessor = function () {
            var t = K.Sort;
            this.config.sort && "object" == typeof this.config.sort.server && (t = K.ServerSort);
            var e, n = this.config.pipeline.getStepsByType(t);
            return n.length > 0 ? e = n[0] : (this.updateSortProcessorFn = this.updateSortProcessor.bind(this), this.store.on("updated", this.updateSortProcessorFn), e = t === K.ServerSort ? new Vt(r({columns: this.store.state}, this.config.sort.server)) : new Xt({columns: this.store.state}), this.config.pipeline.register(e)), e
        }, n.changeDirection = function (t) {
            t.preventDefault(), t.stopPropagation(), this.actions.sortToggle(this.props.index, !0 === t.shiftKey && this.config.sort.multiColumn, this.props.compare)
        }, n.render = function () {
            if (!this.props.enabled) return null;
            var t = this.state.direction, e = "neutral";
            return 1 === t ? e = "asc" : -1 === t && (e = "desc"), b("button", {
                tabIndex: -1,
                "aria-label": this._("sort.sort" + (1 === t ? "Desc" : "Asc")),
                title: this._("sort.sort" + (1 === t ? "Desc" : "Asc")),
                className: nt(et("sort"), et("sort", e), this.config.className.sort),
                onClick: this.changeDirection.bind(this)
            })
        }, e
    }(G), Zt = function (t) {
        function e() {
            for (var e, n = arguments.length, r = new Array(n), i = 0; i < n; i++) r[i] = arguments[i];
            return (e = t.call.apply(t, [this].concat(r)) || this).moveFn = void 0, e.upFn = void 0, e
        }

        i(e, t);
        var n = e.prototype;
        return n.getPageX = function (t) {
            return t instanceof MouseEvent ? Math.floor(t.pageX) : Math.floor(t.changedTouches[0].pageX)
        }, n.start = function (t) {
            var e, n, r, i, o;
            t.stopPropagation(), this.setState({offsetStart: parseInt(this.props.thRef.current.style.width, 10) - this.getPageX(t)}), this.upFn = this.end.bind(this), this.moveFn = (e = this.move.bind(this), void 0 === (n = 10) && (n = 100), function () {
                var t = [].slice.call(arguments);
                r ? (clearTimeout(i), i = setTimeout(function () {
                    Date.now() - o >= n && (e.apply(void 0, t), o = Date.now())
                }, Math.max(n - (Date.now() - o), 0))) : (e.apply(void 0, t), o = Date.now(), r = !0)
            }), document.addEventListener("mouseup", this.upFn), document.addEventListener("touchend", this.upFn), document.addEventListener("mousemove", this.moveFn), document.addEventListener("touchmove", this.moveFn)
        }, n.move = function (t) {
            t.stopPropagation();
            var e = this.props.thRef.current;
            this.state.offsetStart + this.getPageX(t) >= parseInt(e.style.minWidth, 10) && (e.style.width = this.state.offsetStart + this.getPageX(t) + "px")
        }, n.end = function (t) {
            t.stopPropagation(), document.removeEventListener("mouseup", this.upFn), document.removeEventListener("mousemove", this.moveFn), document.removeEventListener("touchmove", this.moveFn), document.removeEventListener("touchend", this.upFn)
        }, n.render = function () {
            return b("div", {
                className: nt(et("th"), et("resizable")),
                onMouseDown: this.start.bind(this),
                onTouchStart: this.start.bind(this),
                onClick: function (t) {
                    return t.stopPropagation()
                }
            })
        }, e
    }(G), Jt = function (t) {
        function e(e, n) {
            var r;
            return (r = t.call(this, e, n) || this).sortRef = {current: null}, r.thRef = {current: null}, r.state = {style: {}}, r
        }

        i(e, t);
        var n = e.prototype;
        return n.isSortable = function () {
            return this.props.column.sort.enabled
        }, n.isResizable = function () {
            return this.props.column.resizable
        }, n.onClick = function (t) {
            t.stopPropagation(), this.isSortable() && this.sortRef.current.changeDirection(t)
        }, n.keyDown = function (t) {
            this.isSortable() && 13 === t.which && this.onClick(t)
        }, n.componentDidMount = function () {
            var t = this;
            setTimeout(function () {
                if (t.props.column.fixedHeader && t.thRef.current) {
                    var e = t.thRef.current.offsetTop;
                    "number" == typeof e && t.setState({style: {top: e}})
                }
            }, 0)
        }, n.content = function () {
            return void 0 !== this.props.column.name ? this.props.column.name : void 0 !== this.props.column.plugin ? b(ht, {
                pluginId: this.props.column.plugin.id,
                props: {column: this.props.column}
            }) : null
        }, n.getCustomAttributes = function () {
            var t = this.props.column;
            return t ? "function" == typeof t.attributes ? t.attributes(null, null, this.props.column) : t.attributes : {}
        }, n.render = function () {
            var t = {};
            return this.isSortable() && (t.tabIndex = 0), b("th", r({
                ref: this.thRef,
                "data-column-id": this.props.column && this.props.column.id,
                className: nt(et("th"), this.isSortable() ? et("th", "sort") : null, this.props.column.fixedHeader ? et("th", "fixed") : null, this.config.className.th),
                onClick: this.onClick.bind(this),
                style: r({}, this.config.style.th, {
                    minWidth: this.props.column.minWidth,
                    width: this.props.column.width
                }, this.state.style, this.props.style),
                onKeyDown: this.keyDown.bind(this),
                rowSpan: this.props.rowSpan > 1 ? this.props.rowSpan : void 0,
                colSpan: this.props.colSpan > 1 ? this.props.colSpan : void 0
            }, this.getCustomAttributes(), t), b("div", {className: et("th", "content")}, this.content()), this.isSortable() && b(Yt, r({
                ref: this.sortRef,
                index: this.props.index
            }, this.props.column.sort)), this.isResizable() && this.props.index < this.config.header.visibleColumns.length - 1 && b(Zt, {
                column: this.props.column,
                thRef: this.thRef
            }))
        }, e
    }(G), Qt = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        i(e, t);
        var n = e.prototype;
        return n.renderColumn = function (t, e, n, r) {
            var i = function (t, e, n) {
                var r = wt.maximumDepth(t), i = n - e;
                return {rowSpan: Math.floor(i - r - r / i), colSpan: t.columns && t.columns.length || 1}
            }(t, e, r);
            return b(Jt, {column: t, index: n, colSpan: i.colSpan, rowSpan: i.rowSpan})
        }, n.renderRow = function (t, e, n) {
            var r = this, i = wt.leafColumns(this.props.header.columns);
            return b(zt, null, t.map(function (t) {
                return t.hidden ? null : r.renderColumn(t, e, i.indexOf(t), n)
            }))
        }, n.renderRows = function () {
            var t = this, e = wt.tabularFormat(this.props.header.columns);
            return e.map(function (n, r) {
                return t.renderRow(n, r, e.length)
            })
        }, n.render = function () {
            return this.props.header ? b("thead", {
                key: this.props.header.id,
                className: nt(et("thead"), this.config.className.thead)
            }, this.renderRows()) : null
        }, e
    }(G), te = function (t) {
        function e() {
            return t.apply(this, arguments) || this
        }

        return i(e, t), e.prototype.render = function () {
            return b("table", {
                role: "grid",
                className: nt(et("table"), this.config.className.table),
                style: r({}, this.config.style.table, {height: this.props.height})
            }, b(Qt, {header: this.props.header}), b(Gt, {
                data: this.props.data,
                status: this.props.status,
                header: this.props.header
            }))
        }, e
    }(G), ee = function (e) {
        function n(t, n) {
            var r;
            return (r = e.call(this, t, n) || this).headerRef = {current: null}, r.state = {isActive: !0}, r
        }

        i(n, e);
        var o = n.prototype;
        return o.componentDidMount = function () {
            0 === this.headerRef.current.children.length && this.setState({isActive: !1})
        }, o.render = function () {
            return this.state.isActive ? b("div", {
                ref: this.headerRef,
                className: nt(et("head"), this.config.className.header),
                style: r({}, this.config.style.header)
            }, b(ht, {position: t.PluginPosition.Header})) : null
        }, n
    }(G), ne = function (e) {
        function n(t, n) {
            var r;
            return (r = e.call(this, t, n) || this).footerRef = {current: null}, r.state = {isActive: !0}, r
        }

        i(n, e);
        var o = n.prototype;
        return o.componentDidMount = function () {
            0 === this.footerRef.current.children.length && this.setState({isActive: !1})
        }, o.render = function () {
            return this.state.isActive ? b("div", {
                ref: this.footerRef,
                className: nt(et("footer"), this.config.className.footer),
                style: r({}, this.config.style.footer)
            }, b(ht, {position: t.PluginPosition.Footer})) : null
        }, n
    }(G), re = function (t) {
        function e(e, n) {
            var r;
            return (r = t.call(this, e, n) || this).configContext = void 0, r.processPipelineFn = void 0, r.configContext = function (t, e) {
                var n = {
                    __c: e = "__cC" + d++, __: null, Consumer: function (t, e) {
                        return t.children(e)
                    }, Provider: function (t) {
                        var n, r;
                        return this.getChildContext || (n = [], (r = {})[e] = this, this.getChildContext = function () {
                            return r
                        }, this.shouldComponentUpdate = function (t) {
                            this.props.value !== t.value && n.some(x)
                        }, this.sub = function (t) {
                            n.push(t);
                            var e = t.componentWillUnmount;
                            t.componentWillUnmount = function () {
                                n.splice(n.indexOf(t), 1), e && e.call(t)
                            }
                        }), t.children
                    }
                };
                return n.Provider.__ = n.Consumer.contextType = n
            }(), r.state = {status: Dt.Loading, header: e.header, data: null}, r
        }

        i(e, t);
        var n = e.prototype;
        return n.processPipeline = function () {
            try {
                var t = this;
                t.props.config.eventEmitter.emit("beforeLoad"), t.setState({status: Dt.Loading});
                var e = function (e, n) {
                    try {
                        var r = Promise.resolve(t.props.pipeline.process()).then(function (e) {
                            t.setState({data: e, status: Dt.Loaded}), t.props.config.eventEmitter.emit("load", e)
                        })
                    } catch (t) {
                        return n(t)
                    }
                    return r && r.then ? r.then(void 0, n) : r
                }(0, function (e) {
                    lt.error(e), t.setState({status: Dt.Error, data: null})
                });
                return Promise.resolve(e && e.then ? e.then(function () {
                }) : void 0)
            } catch (t) {
                return Promise.reject(t)
            }
        }, n.componentDidMount = function () {
            try {
                var t = this, e = t.props.config;
                return Promise.resolve(t.processPipeline()).then(function () {
                    e.header && t.state.data && t.state.data.length && t.setState({header: e.header.adjustWidth(e)}), t.processPipelineFn = t.processPipeline.bind(t), t.props.pipeline.on("updated", t.processPipelineFn)
                })
            } catch (t) {
                return Promise.reject(t)
            }
        }, n.componentWillUnmount = function () {
            this.props.pipeline.off("updated", this.processPipelineFn)
        }, n.componentDidUpdate = function (t, e) {
            e.status != Dt.Rendered && this.state.status == Dt.Loaded && (this.setState({status: Dt.Rendered}), this.props.config.eventEmitter.emit("ready"))
        }, n.render = function () {
            return b(this.configContext.Provider, {value: this.props.config}, b("div", {
                role: "complementary",
                className: nt("gridjs", et("container"), this.state.status === Dt.Loading ? et("loading") : null, this.props.config.className.container),
                style: r({}, this.props.config.style.container, {width: this.props.width})
            }, this.state.status === Dt.Loading && b("div", {className: et("loading-bar")}), b(ee, null), b("div", {
                className: et("wrapper"),
                style: {height: this.props.height}
            }, b(te, {
                ref: this.props.config.tableRef,
                data: this.state.data,
                header: this.state.header,
                width: this.props.width,
                height: this.props.height,
                status: this.state.status
            })), b(ne, null), b("div", {ref: this.props.config.tempRef, id: "gridjs-temp", className: et("temp")})))
        }, e
    }(G), ie = function (t) {
        function e(e) {
            var n;
            return (n = t.call(this) || this).config = void 0, n.plugin = void 0, n.config = new Mt({
                instance: s(n),
                eventEmitter: s(n)
            }).update(e), n.plugin = n.config.plugin, n
        }

        i(e, t);
        var n = e.prototype;
        return n.updateConfig = function (t) {
            return this.config.update(t), this
        }, n.createElement = function () {
            return b(re, {
                config: this.config,
                pipeline: this.config.pipeline,
                header: this.config.header,
                width: this.config.width,
                height: this.config.height
            })
        }, n.forceRender = function () {
            return this.config && this.config.container || lt.error("Container is empty. Make sure you call render() before forceRender()", !0), this.config.pipeline.clearCache(), j(null, this.config.container), j(this.createElement(), this.config.container), this
        }, n.render = function (t) {
            return t || lt.error("Container element cannot be null", !0), t.childNodes.length > 0 ? (lt.error("The container element " + t + " is not empty. Make sure the container is empty and call render() again"), this) : (this.config.container = t, j(this.createElement(), t), this)
        }, e
    }(J), oe = 0, se = [], ae = l.__b, ue = l.__r, le = l.diffed, ce = l.__c, pe = l.unmount;

    function he(t, e) {
        l.__h && l.__h(jt, t, oe || e), oe = 0;
        var n = jt.__H || (jt.__H = {__: [], __h: []});
        return t >= n.__.length && n.__.push({}), n.__[t]
    }

    function fe() {
        se.forEach(function (t) {
            if (t.__P) try {
                t.__H.__h.forEach(_e), t.__H.__h.forEach(me), t.__H.__h = []
            } catch (e) {
                t.__H.__h = [], l.__e(e, t.__v)
            }
        }), se = []
    }

    l.__b = function (t) {
        jt = null, ae && ae(t)
    }, l.__r = function (t) {
        ue && ue(t), Ot = 0;
        var e = (jt = t.__c).__H;
        e && (e.__h.forEach(_e), e.__h.forEach(me), e.__h = [])
    }, l.diffed = function (t) {
        le && le(t);
        var e = t.__c;
        e && e.__H && e.__H.__h.length && (1 !== se.push(e) && Wt === l.requestAnimationFrame || ((Wt = l.requestAnimationFrame) || function (t) {
            var e, n = function () {
                clearTimeout(r), de && cancelAnimationFrame(e), setTimeout(t)
            }, r = setTimeout(n, 100);
            de && (e = requestAnimationFrame(n))
        })(fe)), jt = void 0
    }, l.__c = function (t, e) {
        e.some(function (t) {
            try {
                t.__h.forEach(_e), t.__h = t.__h.filter(function (t) {
                    return !t.__ || me(t)
                })
            } catch (n) {
                e.some(function (t) {
                    t.__h && (t.__h = [])
                }), e = [], l.__e(n, t.__v)
            }
        }), ce && ce(t, e)
    }, l.unmount = function (t) {
        pe && pe(t);
        var e = t.__c;
        if (e && e.__H) try {
            e.__H.__.forEach(_e)
        } catch (t) {
            l.__e(t, e.__v)
        }
    };
    var de = "function" == typeof requestAnimationFrame;

    function _e(t) {
        var e = jt;
        "function" == typeof t.__c && t.__c(), jt = e
    }

    function me(t) {
        var e = jt;
        t.__c = t.__(), jt = e
    }

    function ge(t, e) {
        return !t || t.length !== e.length || e.some(function (e, n) {
            return e !== t[n]
        })
    }

    t.BaseActions = st, t.BaseComponent = G, t.BaseStore = it, t.Cell = V, t.Component = k, t.Config = Mt, t.Dispatcher = Pt, t.Grid = ie, t.PluginBaseComponent = ct, t.Row = Y, t.className = et, t.createElement = b, t.createRef = function () {
        return {current: null}
    }, t.h = b, t.html = $, t.useEffect = function (t, e) {
        var n = he(Ot++, 3);
        !l.__s && ge(n.__H, e) && (n.__ = t, n.__H = e, jt.__H.__h.push(n))
    }, t.useRef = function (t) {
        return oe = 5, function (t, e) {
            var n = he(Ot++, 7);
            return ge(n.__H, e) && (n.__ = t(), n.__H = e, n.__h = t), n.__
        }(function () {
            return {current: t}
        }, [])
    }
});
//# sourceMappingURL=gridjs.umd.js.map
