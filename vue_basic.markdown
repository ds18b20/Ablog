# Vue
简单记录一下最近学习vue过程中搜索的一些小知识点。

## 安装
- 官网找到源文件下载到项目内使用
- 使用在线CDN
无论是本地调用还是在线调用，注意vue氛围development version和production version。
开发版vue.js包含了调试相关的信息，体积比较大，所以上线后应该使用生产版本即vue.min.js。

## 简单使用
下面是自己用到的几个功能：
### {{ message }}
声明式渲染，直接用data中的message以文本形式替换{{ message }}部分。
html部分：
```html
<div id="app">
  {{ message }}
</div>
```
js部分：
```javascript
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})
```
我的理解，主要用在对html中一整块的重写。
### v-bind
可以实现对html中某些属性的绑定。
例如，
```html
<p v-bind:class="abc">xxx</p>
```
abc不再是一个字符串，而是绑定到了data里的abc属性上面了。
在js里更改data的abc属性就可以方便地修改上例中的p标签的class名里。

### v-model
v-model主要是用在表单元素中，它实现了双向绑定。
跟上面的实现相同，实例的data.name发生变化的时候，对应的试图中也会发生变化。但是v-model绑定后，反过来在input中手动输入新的内容，会反过来修改data.name的值，如果在视图中其他地方使用到了data.name，那么这个地方就会因为data.name的变化而变化，从而实现关联动态效果。
> v-model 其实是一个语法糖，这背后其实做了两个操作
v-bind 绑定一个 value 属性
v-on 指令给当前元素绑定 input 事件
在原生表单元素中
<input v-model='something'>
就相当于
<input v-bind:value="something" v-on:input="something = $event.target.value">
当input接收到新的输入，就会触发input事件，将事件目标的value 值赋给绑定的元素

### v-on
v-on可以绑定到某个事件上以监控这个事件的变化。
例如，对click的绑定：
```html
<input v-model="verification_code" type="button" id="code" v-on:click="createCode"  class="uk-button uk-button-default" >

```
对blur的绑定：（实现脱离input输入框后的动作）
```html
 v-on:blur="func_name"
```

### created方法
实现载入vue对象后直接运行指定方法的功能。
```html
Vue.component('graph', {
    props:['graphId','graphData'],
    template: '<canvas></canvas>',
    created: function () {
        alert('{{graphId}}');
    },
    methods: {}
});
```
关于生命周期的拓展：https://vuejs.org/v2/guide/instance.html#Instance-Lifecycle-Hooks

# 参考
https://www.tangshuang.net/3507.html
https://segmentfault.com/a/1190000009492595
https://stackoverflow.com/questions/40676377/run-component-method-on-load-vue-js
