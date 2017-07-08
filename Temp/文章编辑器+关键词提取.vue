<template>
    <div id="detail">
        <Card style="width:320px;margin-left: auto;margin-right: auto">
            <div style="text-align:center">
                <h3>文章编辑器</h3>
            </div>
        </Card>
        <br>
        <Form :model="form" :label-width="80" :rules="articleRules" ref="form">
            <Row>
                <Col span="8">
                <Form-item prop="category" label="类型" style="z-index:999999;width: 100%;float: left">
                    <Select :disabled="!canEdit" v-model="form.category" placeholder="请选择"
                            style="z-index:999999;float: left">
                        <Option value="ggtz">公告通知</Option>
                        <Option value="xzzq">下载专区</Option>
                        <Option value="hydt">行业动态</Option>
                        <Option value="xwzx">新闻资讯</Option>
                        <Option value="zcfg">政策法规</Option>
                        <Option value="xmhz">项目合作</Option>
                    </Select>
                </Form-item>
                </Col>
                <Col span="8">
                <Form-item prop="a_id" label="文章ID" style="">
                    <Input v-model="form.a_id" readonly></Input>
                </Form-item>
                </Col>
                <Col>
                <Button type="error" @click="handleDelete" style="float: right;" v-show="canEdit">删除该文章</Button>
                </Col>
                <Col>
                </Col>
            </Row>

            <Form-item prop="title" label="标题" style="">
                <Input v-model="form.title" placeholder="请输入" :readonly="!canEdit"></Input>
            </Form-item>
            <Form-item prop="keywords" label="标签" style="">
                <Input v-model="form.keywords" placeholder="请输入" :readonly="!canEdit"></Input>
            </Form-item>
            <Form-item>
                <UpImgModal module_name="上传文章图片" :onUploadSuccess="update_news_content" :renamePrefix="form.title" v-show="canEdit">

                </UpImgModal>

            </Form-item>
            <Row>
                <Form-item prop="content">
                    <UMeditor v-if="canEdit" ref="UMeditor" :content="form.content"></UMeditor>
                    <span v-else v-html="form.content"></span>
                </Form-item>
            </Row>
            <br>
            <br>
            <Button type="primary" @click="handleSubmit" style="float: right;width: 180px;" v-show="canEdit">提交</Button>
            <Button type="ghost" @click="autoExtractKeywords" >获取关键词</Button>
            <goback cancelMsg="放弃编辑？" :confirm="canEdit" okMsg="" style="float: left;"></goback>
            <br>
            <br>
        </Form>
        <br>
    </div>
</template>

<script>
    import util from '../../util/utils.js';
    import goback from '../../components/common/trick/goback.vue';
    import UMeditor from '../../components/plugins/UMeditor/UMeditor.vue';
    import UpImgModal from '../../components/common/trick/UpImgModal.vue';
    export default {
        data () {
            return {
                canEdit: G_CheckAdminPermission(17),
                form: {
                    a_id: '',
                    title: '',
                    category: '',
                    content: '',
                    show_time: '',
                    update_time: '',
                    hits: '',
                    ori_url: '',
                    keywords: '',
                },//form数据由detail组件传输过来。
                articleRules: {
                    title: [
                        {required: true, message: '请填写标题', trigger: 'blur'},
                    ],
                },
                initForm: null,     //用来在提交时比对改动的字段
            }
        },
        methods: {
            //            ==================网络相关==================
            handleSubmit(){
                this.form.content = this.$refs.UMeditor.getContent();
                let self = this;

                self.$refs.form.validate((valid) => {
                    if (valid) {
                        let url = req_news_modify;
                        if(self.form.keywords === ''){
                            self.form.keywords = self.autoExtractKeywords();
                        }
                        self.form.update_time = new Date().getTime();
                        self.form.update_keys = self.getChangedFields();
                        console.log('submit form',self.form);
                        self.$axios.post(url, self.form).then(result => {
                            if (result && result.data && result.data.code == 200) {
                                if(self.form.action === 'add'){
                                    self.$Message.info('添加该新闻成功');
                                    self.form.action = 'update';//已添加到服务器，客户端页面不变，但action改为update。
                                }
                                else{
                                    self.$Message.info('修改该新闻成功');
                                }
                            } else {
                                self.$Message.error('添加新闻失败');
                            }
                        });
                    } else {
                        this.$Message.error('表单验证失败!');
                    }
                })
            },
            handleDelete(){
                this.$Modal.confirm({
                    title: '确认删除？',
                    onOk: () => {
//                        // 删除
                        this.$axios.post(req_news_modify, {action: "delete", a_id: this.form.a_id})
                            .then(result => {
                                if (result && result.data && result.data.code == 200) {
                                    this.$Message.info('删除该文章成功');
                                    G_SetStore('gobackwithme', 'yes');
                                    window.history.go(-1);
                                }
                            })
                    },
                    onCancel: () => {
                        this.$Message.info('您已取消删除');
                    },
                    content: `<strong>文章ID</strong>: ${this.form.a_id}<br><strong>标题</strong>: ${this.form.title}<br>类别: ${this.form.category}<br>`
                });
            },
            update_form_data(){
                let _params = this.$route.params;
                let url = req_news_fetch_news_detail_info;
                if (url.charAt(url.length - 1) !== '&') {
                    url += "&"
                }
                if (_params.itemId) {
                    url += "a_id=" + _params.itemId;
                }
                this.$axios.get(url)
                    .then(result => {
                        if (result && result.data && result.data.code == 200) {
                            this.initForm = result.data.data;
                            let data = result.data.data;
                            this.form.title = data.title;
                            this.form.category = data.category;
                            this.form.content = data.content;
                            this.form.a_id = data.a_id;
                            this.form.ori_url = data.ori_url;
                            this.form.keywords = data.keywords;
                            this.form.hits = data.hits;
                            this.form.update_time = data.update_time;
                            this.form.pics = data.pics;
                            if(data.keywords !== '' && data.keywords.length > 0){
                                this.form.has_keywords = true;
                            }
                        }
                    })
            },

            //            ==================网络相关==================


            //            ==================编辑器相关==================

            getAllHtml() {
                alert(UM.getEditor('editor').getAllHtml())
            },
            getContent() {
                var arr = [];
                arr.push("使用editor.getContent()方法可以获得编辑器的内容");
                arr.push("内容为：");
                arr.push(UM.getEditor('editor').getContent());
                alert(arr.join("\n"));
            }, isFocus() {
                alert(um.isFocus())
            }, doBlur() {
                um.blur()
            },  setContent(isAppendTo) {
                var arr = [];
                arr.push("使用editor.setContent('欢迎使用umeditor', true)方法可以设置编辑器的内容");
                UM.getEditor('editor').setContent('欢迎使用umeditor', isAppendTo);
                alert(arr.join("\n"));
            }, setDisabled() {
                UM.getEditor('editor').setDisabled('fullscreen');
                disableBtn("enable");
            }, setEnabled() {
                UM.getEditor('editor').setEnabled();
                enableBtn();
            }, getText() {
                //当你点击按钮时编辑区域已经失去了焦点，如果直接用getText将不会得到内容，所以要在选回来，然后取得内容
                var range = UM.getEditor('editor').selection.getRange();
                range.select();
                var txt = UM.getEditor('editor').selection.getText();
                alert(txt)
            }, getContentTxt() {
                var arr = [];
                arr.push("使用editor.getContentTxt()方法可以获得编辑器的纯文本内容");
                arr.push("编辑器的纯文本内容为：");
                arr.push(UM.getEditor('editor').getContentTxt());
                alert(arr.join("\n"));
            }, hasContent() {
                var arr = [];
                arr.push("使用editor.hasContents()方法判断编辑器里是否有内容");
                arr.push("判断结果为：");
                arr.push(UM.getEditor('editor').hasContents());
                alert(arr.join("\n"));
            }, setFocus() {
                UM.getEditor('editor').focus();
            }, deleteEditor() {
                disableBtn();
                UM.getEditor('editor').destroy();
            }, disableBtn(str) {
                var div = document.getElementById('btnContainer');
                var btns = UM.dom.domUtils.getElementsByTagName(div, "button");
                for (var i = 0, btn; btn = btns[i++];) {
                    if (btn.id == str) {
                        UM.dom.domUtils.removeAttributes(btn, ["disabled"]);
                    } else {
                        $(btn).attr("disabled", true).addClass("disabled");
                    }
                }
            }, enableBtn() {
                var div = document.getElementById('btnContainer');
                var btns = UM.dom.domUtils.getElementsByTagName(div, "button");
                for (var i = 0, btn; btn = btns[i++];) {
                    $(btn).removeAttr("disabled").removeClass("disabled");
                }
            },
            //            ==================编辑器相关==================


            //          关键词自动提取，图片自动插入
            autoExtractKeywords(){
                let content = this.getContentTxt(); //获取待提取的正文纯文本
                let keyObj = new Array;
                let name = []; //关键词name
                let indexOfDefaultKeys =[];  //关键词在词表中位置
                let wordFreq = [];    //关键词在本篇目中的出现次数
                let weight = [];  //关键词权重值
                let stopkey = [];  //关键词是否为停用词 [boolean]

                let keys = this.getInitKeywords();   //初始化关键词表
                console.log('keys',keys);
                this.extractKey(content,keys,name,indexOfDefaultKeys,stopkey);   //获取关键词。其在【预设关键词词库】位置，是否停用

                this.timeCounter(wordFreq,indexOfDefaultKeys);      //获取词频=》权重
                this.getWeights(wordFreq,weight);

                this.toObject(keyObj,indexOfDefaultKeys,wordFreq,weight,stopkey,name);
                console.log('xxxxx结果，依次为 TAGS=最终标签，关键词，关键词权重，停用词，阈值，关键词中可作为标签的词，您选择的标引深度，最终的标签',this.outResult(keyObj=keyObj,weight=weight,stopkey=stopkey,name=name));

                return this.outResult(keyObj,indexOfDefaultKeys,wordFreq,weight,stopkey,name,content)[0]
            },
            getInitKeywords(){
                return this.getDefaultKeywords().concat(this.getDefaultKeydrop())
            },
            extractKey(content,keys,name,indexOfDefaultKeys,stopkey,maxLenOfKey=6){
                //content:
                //keys: [str], 【预设关键词词库】 + 【预设停用词词库】
                //name: 【str],关键词列表
                //indexOfDefaultKeys: [int], 关键词在 【预设关键词词库】 中的位置索引。
                //stopkey:  [],停用词
                //maxLenOfKey: int, 关键词的最大长度
                let cntLen = content.length;
                let keyLen = this.getDefaultKeywords().length;
                for(let k=cntLen; k>0; k--){
                    label:
                    for(let j=maxLenOfKey; j>0; j--){ //通过最大关键字长度控制循环
                        let strkey = content.substr(k-j,j);
                        //确定预检索字符串，cntLen - j是位置， j是长度
                        for(let i=0; i<keys.length; i++){
                            if(keys[i] == strkey){//如果现有关键字与字库匹配
                                name.push(strkey);
                                indexOfDefaultKeys.push(i);
                                if(i>keyLen){
                                    stopkey.push(false);
                                }
                                else{
                                    stopkey.push(true);
                                }
                                k -= j;
                                k++;
                                break label;
                            }
                        }
                    }
                }
            },
            timeCounter(wordFreq,indexOfDefaultKeys){
              let k=0;
              for(let i=0; i<indexOfDefaultKeys.length; i++){
                  for(let j=0; j<indexOfDefaultKeys.length; j++) {
                      if (indexOfDefaultKeys[i] == indexOfDefaultKeys[j]) {
                          k += 1;
                      }
                  }
                  wordFreq.push(k);
                  k = 0;
              }
            },
            getWeights(wordFreq,weight){
                //权重公式可改进
                let l,j,n;
                for(let i=0; i<wordFreq.length; i++){
                    l = wordFreq[i] / 1;
                    j = Math.log(l);
                    n = wordFreq[i] * j;
                    weight.push(n.toFixed(3));
                }
            },
            toObject(keyObj,indexOfDefaultKeys,wordFreq,weight,stopkey,name){
              keyObj['name'] = name;
              keyObj['indexOfDefaultKeys'] = indexOfDefaultKeys;
              keyObj['weight'] = weight;
              keyObj['stopkey'] = stopkey;
              keyObj['wordFreq'] = wordFreq;
            },
            outResult(keyObj,weight,stopkey,name,inweight=3,indesc=3){

                //inweight 阈值
                //indesc 标引深度

                console.log('outResult',keyObj);

                let outkeyarray = [], outweightarray = [];
                for(let i=0;i<name.length;i++) {
                    if(keyObj["stopkey"][i] === true) {
                        outkeyarray.push(keyObj["name"][i]);
                        outweightarray.push(keyObj["weight"][i]);
                    }

                }

                for(let i=0;i<outkeyarray.length;i++) {
                    for(let j=outkeyarray.length;j>i;j--) {
                        if(outkeyarray[i] === outkeyarray[j]) {
                            outkeyarray = outkeyarray.slice(0,j).concat(outkeyarray.slice(j+1,outkeyarray.length));
                            outweightarray = outweightarray.slice(0,j).concat(outweightarray.slice(j+1,outweightarray.length));
                        }
                    }
                }

                let outkey = outkeyarray.join(",");
                let outweight = outweightarray.join(",");
                let outkeystoparray = [];
                for(let i=0;i<name.length;i++) {

                    if(keyObj["stopkey"][i] === false) {
                        outkeystoparray.push(keyObj["name"][i]);
                    }
                }

                let outstop = outkeystoparray.join(",");
                let outval = inweight;

                let outwordarray = [],outweightarray1 = [];
                for(let i=0;i<outkeyarray.length;i++) {
                    if(outweightarray[i]>inweight) {
                        outwordarray.push(outkeyarray[i]);
                        outweightarray1.push(outweightarray[i])
                    }
                }

                let outword = outwordarray.join(",");
                let outdeep = indesc;
                for(let i=0;i<outwordarray.length;i++) {
                    let k,l;
                    for(let j=i+1;j<outwordarray.length;j++) {
                        if(outweightarray1[i]<outweightarray1[j]) {
                            k=outweightarray1[i];
                            outweightarray1[i]=outweightarray1[j];
                            outweightarray1[j]=k;
                            l=outwordarray[i];
                            outwordarray[i]=outwordarray[j];
                            outwordarray[j]=l;
                        }
                    }

                }

                outwordarray = outwordarray.slice(0,indesc);
                let outkeyword = outwordarray.join(",");
                let outtags = outwordarray.join(",");

                return [outtags,outkey,outweight,outstop,outval,outword,outdeep,outkeyword];
            },
            getDefaultKeydrop(){
              return ["的","你",];
            },
            getDefaultKeywords(){
//                let default_keywords = {"title":"中国电子商务协会-中国电子商务师考试报名平台","key":"电子商务师,电子商务培训,电子商务师考试,电子商务师培训","des":"中国电子商务师考试报名平台是中国电子商务协会的下级单位，负责在全国组织电子商务人才培养工程。服务范围包括中国电子商务师职业资格（水平）考试、网上报名、电子商务培训、分数查询等。"};
//                return default_keywords.key;
              return ["电子商务师","法律法规","贸易","制裁","改造","中国","经济","中国经济","拯救","美国","美国经济","整顿","银行业","银行","速度","温家宝","美中","逆差","贸易逆差","结构性","转移性","机电","进出口","商会","彩电","倾销","税率","交涉","东北","亚洲","亚洲经济","论坛","增长","失业率","失业","回落","批评","限制","纺织品","进口","加拿大","统计","移民","收入","差异","中央银行","中央","商业银行","政策","措施","经济发展","发展","日本","日本经济","复苏","决定","锻铸","铁管","管件","征收","反倾销","垄断","倾销税","联合国","联合","实施","伊拉克","石油","食品","计划","发展中国家","发达国家","国家","家电","电信","产业","电子","信息","产销","俄罗斯","检察官","检察","首富","犯罪","调查","结束","欧盟","争端","投资","受挫","改革","委员会","委员","实行","临时","价格","干预","施行","美联储","警告","通货膨胀","膨胀","下滑","衰退","季度","扬言","演示简单","后台"];
            },
            getPlainTxt() {
                // 含&lt;等
                return (UM.getEditor(this.$refs.UMeditor.domId).getPlainTxt());
            },
            getContentTxt(){
                // 没有html符号,推荐使用该方法。
                return (UM.getEditor(this.$refs.UMeditor.domId).getContentTxt());
            },
            insertHtml(value) {
                this.$refs.UMeditor.um.execCommand('insertHtml', value)
            },
            update_news_content(img_url){
                console.log('((((((((((', img_url);
                this.insertHtml('<img src="' + img_url + '" width="600px"/>');
            },
            getChangedFields(){
                let update_keys = [];
                for(let i in this.initForm){
                    if(this.form.hasOwnProperty(i) && this.initForm[i] !== this.form[i]){
                        update_keys.push(i);
                    }
                å
                if(update_keys.indexOf('update_time') < 0){
                    update_keys.push('update_time');
                }
                return update_keys;
            }
            //            ==================功能相关==================

        },

        computed: {},
        created: function () {
            G_RemoveStore('gobackwithme');
        }
        ,
        mounted: function () {
            if (this.$route.params.hasOwnProperty('itemId')) {
                // modify
                this.update_form_data();
                this.form.action = "update"
            } else {
                // add
                this.form.action = "add"
            }
            window.onkeydown = function (event) {
                let e = event || window.event;
                let keyCode = e.keyCode || e.which;
                switch (keyCode){
                    case 80:
                        break;
                    case 8:
                        if (!this.$refs.UMeditor.um.isFocus()) {
                            event.preventDefault();
                        }
                        break;
                }

            }
        },
        components: {
            UMeditor,
            goback,
            UpImgModal,
        }
    }




</script>

<style scoped>
    #tree {
        font-family: "Microsoft YaHei" ! important
    }

    #tree a:hover {
        font-style: italic;
    }
</style>


