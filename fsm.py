from graphviz import Digraph

state_set = [['initial'],
    ['show_tutorial', 'to_en_ja', 'to_zh_ja', 'to_zh_en'],
    ['zh_to_en_result', 'zh_to_ja_result', 'en_to_zh_result', 'en_to_ja_result', 'ja_to_zh_result', 'ja_to_en_result'],
    ['zh_en_ex', 'zh_ja_ex', 'en_zh_ex', 'en_ja_ex', 'ja_zh_ex', 'ja_en_ex'],
    ['check_zh_ex', 'check_en_ex', 'check_ja_ex'],
    ['no_ex']
]
colors = ['black', 'blue', 'green', 'orange', 'yellow', 'red']

def e(a, b, l, c):
    dot.edge(a, b, label=l, color=c)

dot = Digraph(format="png")
dot.attr(rankdir='LR', size='8,5')

for states, color in zip(state_set, colors):
    for state in states:
        dot.node(name=state, label=state, color=color)
# 
e('initial', 'show_manual', '嗨', 'black')
e('show_tutorial', 'to_en_ja', ':中文', 'black')
e('show_tutorial', 'to_zh_ja', ':英文', 'black')
e('show_tutorial', 'to_zh_en', ':日文', 'black')
e('initial', 'to_en_ja', ':中文', 'black')
e('initial', 'to_zh_ja', ':英文', 'black')
e('initial', 'to_zh_en', ':日文', 'black')
# 
e('to_en_ja', 'zh_to_en_result', '幫我翻英文', 'black')
e('to_en_ja', 'zh_to_ja_result', '幫我翻日文', 'black')

e('to_zh_ja', 'en_to_zh_result', '幫我翻中文', 'black')
e('to_zh_ja', 'en_to_ja_result', '幫我翻日文', 'black')

e('to_zh_en', 'ja_to_zh_result', '幫我翻中文', 'black')
e('to_zh_en', 'ja_to_en_result', '幫我翻英文', 'black')
# 
e('zh_to_en_result', 'check_zh_ex', '看例句', 'black')
e('check_zh_ex', 'no_ex', '如果沒例句', 'black')
e('zh_en_ex', 'check_zh_ex', '下一句', 'black')
e('check_zh_ex', 'zh_en_ex', '如果有中文例句', 'black')
e('zh_en_ex', 'to_en_ja', '嘗試其他翻譯方式', 'black')

e('zh_to_ja_result', 'check_zh_ex', '看例句', 'black')
e('zh_ja_ex', 'check_zh_ex', '下一句', 'black')
e('check_zh_ex', 'zh_ja_ex', '如果有中文例句', 'black')
e('zh_ja_ex', 'to_en_ja', '嘗試其他翻譯方式', 'black')

e('en_to_zh_result', 'check_en_ex', '看例句', 'black')
e('check_en_ex', 'no_ex', '如果沒例句', 'black')
e('en_zh_ex', 'check_en_ex', '下一句', 'black')
e('check_en_ex', 'en_zh_ex', '如果有英文例句', 'black')
e('en_zh_ex', 'to_zh_ja', '嘗試其他翻譯方式', 'black')

e('en_to_ja_result', 'check_en_ex', '看例句', 'black')
e('en_ja_ex', 'check_en_ex', '下一句', 'black')
e('check_en_ex', 'en_ja_ex', '如果有英文例句', 'black')
e('en_ja_ex', 'to_zh_ja', '嘗試其他翻譯方式', 'black')

e('ja_to_zh_result', 'check_ja_ex', '看例句', 'black')
e('check_ja_ex', 'no_ex', '如果沒例句', 'black')
e('ja_zh_ex', 'check_ja_ex', '下一句', 'black')
e('check_ja_ex', 'ja_zh_ex', '如果有日文例句', 'black')
e('ja_zh_ex', 'to_zh_en', '嘗試其他翻譯方式', 'black')

e('ja_to_en_result', 'check_ja_ex', '看例句', 'black')
e('check_ja_ex', 'ja_en_ex', '下一句', 'black')
e('check_ja_ex', 'ja_zh_ex', '如果有日文例句', 'black')
e('ja_en_ex', 'to_zh_en', '嘗試其他翻譯方式', 'black')
# 
e('no_ex', 'initial', '換一個', 'black')
#

print(dot.source)
dot.render(filename='fsm', directory="./imgs",view=False)
dot.render(filename='fsm', directory="./static",view=False)