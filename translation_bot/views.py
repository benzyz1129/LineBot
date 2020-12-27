from random import randint, random
from typing import Callable
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    PostbackEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    ConfirmTemplate,
    PostbackTemplateAction, 
    ImageSendMessage,
    actions
)

from .crawler import Crawler
from .gooleapi import Googleapi
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("message : "+event.message.text)
                if event.message.text in ['嗨', '哈囉', '你好', 'Hi', 'HI', 'hi', 'Hello', 'HELLO', 'hello']:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=
                            "你/妳好 我是 Translation Bot\n\n"+
                            "互動方法 : \n\n"+
                            "1. 請輸入想翻譯的詞句，並以 ':' 符號開頭，這樣我才知道這是您想要翻譯的詞句喔！\n\n"+
                            "例如 [:Hello]\n\n"
                            "2. 選擇翻譯目標語言，目前提供中日英三種語言之間的交互翻譯。\n\n"+
                            "3. 選擇 “嘗試其他翻譯方式” 繼續翻譯或 “翻譯其他詞句” 換一個吧！\n\n"+
                            "4. 如果輸入單詞的話，可以選擇 “例句” 查看中日英的造句範例喔！"
                        )
                    )
                elif event.message.text[0] in [':', '：']:  
                    input = event.message.text[1:]
                    translator = Googleapi(input)
                    input_lang = translator.detect()
                    if input_lang == 'zh-CN':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='偵測語言 : 中文',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    text='想要翻譯成哪種語言呢？',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻英文',
                                            text='幫我翻英文',
                                            data='@en' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻日文',
                                            text='幫我翻日文',
                                            data='@ja' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                    elif input_lang == 'en':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='偵測語言 : 英文',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    text='想要翻譯成哪種語言呢？',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻中文',
                                            text='幫我翻中文',
                                            data='@zh' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻日文',
                                            text='幫我翻日文',
                                            data='@ja' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                    elif input_lang == 'ja':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='偵測語言 : 日文',
                                    text='想要翻譯成哪種語言呢？',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻中文',
                                            text='幫我翻中文',
                                            data='@zh' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻英文',
                                            text='幫我翻英文',
                                            data='@en' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                    else:
                        line_bot_api.reply_message( 
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title="目前沒有提供此語言的翻譯耶...",
                                    text="換一個試試看吧！",
                                    thumbnail_image_url="https://github.com/benzyz1129/LineBot/blob/master/imgs/sorry.png?raw=True",
                                    actions=[
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                elif event.message.text[:3] == 'fsm':
                    line_bot_api.reply_message( 
                        event.reply_token,
                        ImageSendMessage("https://github.com/benzyz1129/LineBot/blob/master/imgs/fsm.png?raw=True",
                                         "https://github.com/benzyz1129/LineBot/blob/master/imgs/fsm.png?raw=True")
                    )
                elif event.message.text not in ['幫我翻中文', '幫我翻英文', '幫我翻日文', '看例句', '嘗試其他翻譯方式', '換一個',\
                                                '請輸入想翻譯的詞句！\n(以 : 開頭)', "下一句", "請再次輸入想翻譯的詞句~" ]:
                    line_bot_api.reply_message( 
                        event.reply_token,
                        TextSendMessage(text="請輸入想翻譯的詞句！\n(以 : 開頭)")
                    )
                # else:
                #     line_bot_api.reply_message( 
                #         event.reply_token,
                #         TextSendMessage(text="輸入“嗨” 或 “hi” 查看使用說明")
                #     )
                        
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                print("postback : "+event.postback.data)
                if event.postback.data[0] == '@':
                    target_lang = event.postback.data[1:3]
                    if target_lang == 'zh': target_lang_ = 'zh-TW'
                    else: target_lang_ = target_lang

                    input = event.postback.data[3:]
                    translator = Googleapi(input)
                    input_lang = translator.detect()
                    if input_lang == 'zh-CN': input_lang = 'zh'

                    if input_lang == 'zh':input_lang_ = '中'
                    elif input_lang == 'en':input_lang_ = '英'
                    else: input_lang_ = '日'

                    translated_result = translator.translate(target_lang_)
                    if target_lang_ == 'zh-TW':target_lang_ = '中'
                    elif target_lang_ == 'en':target_lang_ = '英'
                    elif target_lang_ == 'ja':target_lang_ = '日'

                    line_bot_api.reply_message(  # 後續動作
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title=input_lang_ + "翻" + target_lang_ + " 結果 : ",
                                text=translated_result,
                                thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                actions=[
                                    PostbackTemplateAction(
                                        label='看例句',
                                        text='看例句',
                                        data='$' + target_lang + '|' + input_lang + '|' + translated_result + '|' + input + "|0"
                                    ),
                                    PostbackTemplateAction(
                                        label='嘗試其他翻譯方式',
                                        text='嘗試其他翻譯方式',
                                        data='#' + input
                                    ),
                                    PostbackTemplateAction(
                                        label='換一個',
                                        text='換一個',
                                        data='!'
                                    )
                                ]
                            )
                        )
                    )
                elif event.postback.data[0] == '#':
                    input = event.postback.data[1:]
                    translator = Googleapi(input)
                    input_lang = translator.detect()
                    if input_lang == 'zh-CN':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='欲翻譯詞句 : [ ' + input + ' ]',
                                    text='想要翻譯成哪種語言呢？',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻英文',
                                            text='幫我翻英文',
                                            data='@en' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻日文',
                                            text='幫我翻日文',
                                            data='@ja' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                    elif input_lang == 'en':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='欲翻譯詞句 : [ ' + input + ' ]',
                                    text='想要翻譯成哪種語言呢？',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻中文',
                                            text='幫我翻中文',
                                            data='@zh' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻日文',
                                            text='幫我翻日文',
                                            data='@ja' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                    elif input_lang == 'ja':
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='欲翻譯詞句 : [ ' + input + ' ]',
                                    text='想要翻譯成哪種語言呢？',
                                    thumbnail_image_url='https://github.com/benzyz1129/LineBot/blob/master/imgs/icon.png?raw=True',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='幫我翻中文',
                                            text='幫我翻中文',
                                            data='@zh' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='幫我翻英文',
                                            text='幫我翻英文',
                                            data='@en' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
                elif event.postback.data == '!':
                    line_bot_api.reply_message( 
                        event.reply_token,
                        TextSendMessage(
                            text="請再次輸入想翻譯的詞句"
                        )
                    )
                elif event.postback.data[0] == '$':
                    data = event.postback.data[1:]
                    data = data.split('|')
                    print(data)
                    translated_lang = data[0]
                    input_lang = data[1]
                    translated_result = data[2]
                    input = data[3]
                    index = int(data[-1])
                    crawler = Crawler(translated_lang, translated_result) # get example
                    examples = crawler.crawl()
                    remind = 0
                    # print(examples)
                    if examples != []:
                        output = ""
                        if index == len(examples): 
                            index -= 1
                            remind = 1
                        s1 = examples[index]
                        translator = Googleapi(s1)
                        if translated_lang == 'zh': s1 = "[中] " + s1
                        elif translated_lang == 'en': s1 = "[英] " + s1
                        elif translated_lang == 'ja': s1 = "[日] " + s1

                        if translated_lang == "zh":
                            if input_lang == "en":
                                s2 = translator.translate("en")
                                s2 = "[英] " + s2
                            elif input_lang == "ja":
                                s2 = translator.translate("ja")
                                s2 = "[日] " + s2
                            else: 
                                s2 = "invalid"
                                print("invalid input lang")
                        elif translated_lang == "en":
                            if input_lang == "zh":
                                s2 = translator.translate("zh-TW")
                                s2 = "[中] " + s2
                            elif input_lang == "ja":
                                s2 = translator.translate("ja")
                                s2 = "[日] " + s2
                            else: 
                                s2 = "invalid"
                                print("invalid input lang")
                        elif translated_lang == "ja":
                            if input_lang == "zh":
                                s2 = translator.translate("zh-TW")
                                s2 = "[中] " + s2
                            elif input_lang == "en":
                                s2 = translator.translate("en")
                                s2 = "[英] " + s2
                            else: 
                                s2 = "invalid"
                                print("invalid input lang")
                        else: s2 = "invalid lang"
                                
                        output += s2+"\n"+s1
                        
                        if remind == 1: output = f"“ {translated_result} ” 的例句 {index+1}/{len(examples)}\n\n" + output + "\n\n(已經沒有例句囉，換一個試試看吧！)"
                        else: output = f"“ {translated_result} ” 的例句 {index+1}/{len(examples)}\n\n" + output

                        line_bot_api.reply_message( 
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ConfirmTemplate(
                                    text=output,
                                    actions=[
                                        PostbackTemplateAction(
                                            label='嘗試其他翻譯方式',
                                            text='嘗試其他翻譯方式',
                                            data='#' + input
                                        ),
                                        PostbackTemplateAction(
                                            label='下一句',
                                            text='下一句',
                                            data='$' + translated_lang + '|' + input_lang + '|' + translated_result + '|' + input + '|' + f"{index+1}"
                                        )
                                    ]
                                )
                            )
                        )
                    else: 
                        line_bot_api.reply_message( 
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title="沒有例句了...",
                                    text="輸入單詞會有較多範例造句喔！",
                                    thumbnail_image_url="https://github.com/benzyz1129/LineBot/blob/master/imgs/sorry.png?raw=True",
                                    actions=[
                                        PostbackTemplateAction(
                                            label='換一個',
                                            text='換一個',
                                            data='!'
                                        )
                                    ]
                                )
                            )
                        )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()