import os, sys

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *
from Managers.statementManager import *

"""
【會自動學習的可能組合】
[（文字A）→（文字回答A／關鍵字回答A／圖片回答A）→（文字B）→（文字回答B／關鍵字回答B／圖片回答B）]
[（文字A）→（文字回答A／關鍵字回答A／圖片回答A）→（貼圖B／位置B）→（貼圖回答B／位置回答B）]
[（貼圖A／位置A）→（貼圖回答A／位置回答A）→（文字B）→（文字回答B／關鍵字回答B／圖片回答B）]
[（貼圖A／位置A）→（貼圖回答A／位置回答A）→（貼圖B／位置B）→（貼圖回答B／位置回答B）]

##加權模型所有組合
O [（文字A）→（文字回答A／關鍵字回答A／圖片回答A）] ※設 文字回答A==valid
X [（貼圖A／位置A）→（貼圖回答A／位置回答A）]

##接話模型所有組合
O [（文字回答A）→（文字B）] ※設 all([文字回答A, 所有回答B]==valid) && all([文字回答A, 所有回答B]!=關鍵字)
X [（文字回答A）→（貼圖B／位置B）]
X [（關鍵字回答A／圖片回答A／貼圖回答A／位置回答A）→（文字B／貼圖B／位置B）]

##同義模型所有組合
O [（文字A）→（文字回答B／關鍵字回答B／圖片回答B）] ※設 文字回答A==不懂 && 所有回答B==valid
X [（文字A）→（貼圖回答B／位置回答B）]
X [（貼圖A／位置A）→（文字回答B／關鍵字回答B／圖片回答B／貼圖回答B／位置回答B）]
"""

##手動反饋學習
def feedback_learn_model(key, res):
    #學習 [key → 文字res／關鍵字res／圖片res]
    rand = 1 if res in ['樹懶', '抽籤'] else 0
    firstIndex = 0 if not rand else 2
    adjust_priority(1, key[firstIndex:], res)

##手動反饋學習
def feedback_abandon_model(key, res):
    #降權重 [key → 文字res／關鍵字res／圖片res]
    rand = 1 if res in ['樹懶', '抽籤'] else 0
    firstIndex = 0 if not rand else 2
    adjust_priority(-2, key[firstIndex:], res)

##自動學習模型
# def auto_learn_model(GET_EVENT):
#     message = GET_EVENT["lineMessage"]
#     replyLog = GET_EVENT["replyLog"]
#     channelPK = GET_EVENT["channelPK"]
#     if replyLog[1]:
#         #【加權模型】若 本次回答==valid 則學習 [文字A → 文字回答A／關鍵字回答A／圖片回答A]
#         rand = 1 if message[0:2] in ['樹懶', '抽籤'] else 0
#         firstIndex = 0 if not rand else 2
#         chat_valid_reply(message[firstIndex:], replyLog[0]) 

#         if(get_replied(channelPK, 1) and get_received(channelPK, 1)):
#             #【接話模型】若 all(上次回答、本次回答==valid) && all(上次回答、本次回答!=關鍵字) && 上次回答類型==文字 則學習 [文字回答A → 文字B] && 上次回答!=本次收到
#             if get_replied(channelPK, 1)[0]['type']=='text' and get_replied(channelPK, 1)[0]['valid']==2 and replyLog[1]==2 and get_replied(channelPK, 1)[0]['message']!=message[firstIndex:]:
#                 chat_valid_reply(get_replied(channelPK, 1)[0]['message'], message[firstIndex:])
            
#             #【同義模型】若 上次回答==聽不懂 && 本次回答==valid 則學習 [文字A → 文字回答B／關鍵字回答B／圖片回答B]
#             # if get_replied(channelPK, 1)[0]['message']=='我聽不懂啦！':
#             #     chat_valid_reply(get_received(channelPK, 1)[0]['message'], replyLog[0])