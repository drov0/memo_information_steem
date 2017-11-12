# This will be a function-based helper for storing information in transactions on the steem blockchain
# This will not try to interperet the data
from websocket import create_connection
from steem import Steem




def retrieve(keyword="", account="anarchyhasnogods",sent_to="randowhale", position=-1, keyword_and_account = False, recent = 1, step = 5000):
    node_connection = create_connection("wss://steemd-int.steemit.com")
    s = Steem(node=node_connection)
    memo_list = []
    if position > -1:
        # This returns the memo based on a saved position
        return get_memo(s.get_account_history(sent_to, position, 1))


    else:
        # If the first is 0, it checks the first one with the keyword or account
        #(or and depending on keyword and account)
        found = True
        memo_list = []
        # This gets the total amount of items in the accounts history
        # This it to prevent errors related to going before the creation of the account
        size = s.get_account_history(sent_to,-1,0)[0][0]
        position = size
        if position < 0:
            position = step
        while found:
            print(position)
            # Checks if the

            if recent > 0 and len(memo_list) > 0:
                if len(memo_list) >= recent:
                    break

            history = s.get_account_history(sent_to, position, step)
            memos = get_memo(history)
            for i in memos:
                has_keyword = False
                if keyword != "":
                    i[2].split(keyword)
                    if type(i[2]) == list:
                        for seg in i[2]:
                            if seg != keyword:
                                i[2] +=seg
                        has_keyword = True
                has_account = i[1] == account
                #print(i[1], account)

                if keyword_and_account:
                    if has_keyword and has_account:
                        memo_list.append(i)
                else:
                    if has_account or has_keyword:
                        #print("added")
                        memo_list.append(i)






            if position ==step+1:

                break

            elif position-step < step:
                position = step+1

            else:
                position -=step


        return memo_list





    # This checks if it has the keyword or is by the account











def get_memo(history_list):
    print(history_list)
    memos = []
    for i in history_list:
        memo = []
        for ii in i:

            if type(ii) == dict:
                try:

                    if ii['op'][0] == 'transfer':
                        memo.append(ii['op'][1]['from'])

                        memo.append(ii['op'][1]['memo'])
                        #print(ii)
                        #print(memo)
                        memos.append(memo)

                    else:
                        memo = []
                except:
                    pass
            if type(ii) == int:

                memo.append(ii)
    #print(memos)
    return memos




#node_connection = create_connection("wss://steemd-int.steemit.com")
#s = Steem(node=node_connection)
#print(get_memo(s.get_account_history("anarchyhasnogods",-2000, 1000)))
print(retrieve(keyword="iron"))