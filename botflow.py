from my.db2 import db
import re
import sqlite3

def process_data(message, userid, filepath=None, accept_all_flag = True, with_numbers_flags_list = [True,True], case=False):
    if case==False:
        message = message.lower()
    conn = sqlite3.connect(filepath)
    extr = db(conn).read('data', filters = {'userid': userid})
    if len(extr) == 0:
        return None
    elif len(extr) == 1:
        prv = extr[0][2]
        cur = extr[0][3]
        nxt = extr[0][4]
        n = extr[0][5]
    check_prevnext_flag = False
    nonefound_flag = False
    found_flag = False

    with_numbers_flag = False
    with_numbers_jump_flag = False
    if with_numbers_flags_list[0] == True:
        with_numbers_flag = True
        if with_numbers_flags_list[1] == True:
            with_numbers_jump_flag = True

    if accept_all_flag == True:
        if message in prv+cur+nxt:
            #delete the entry
            return [True,message]
        else:
            check_prevnext_flag = True
    else:
        if message in cur:
            #delete the entry
            return [True,message]
        else:
            check_prevnext_flag = True
            """
            if message.lower().startswith('prev'):
                pass
            elif bool(re.match('prev',message,re.I)):
                pass
            """

        if check_prevnext_flag == True:
            if with_numbers_flag == True:
                reg_res = re.match('prev\((\d*)\)',message.strip(),re.I)
                if reg_res!=None:
                    nombre = reg_res[1]
                    if len(prv)%n==0:
                        num = int(len(prv)/n)
                    else:
                        num = int(len(prv)/n)+1
                    if with_numbers_jump_flag == True:
                        if nombre <= num:
                            return [True,message]
                        else:
                            return [False,message]
                    else:
                        if nombre == num:
                            return [True,message]
                        else:
                            return [False,message]

                else:
                    reg_res2 = re.match('next\((\d*)\)',message.strip(),re.I)
                    if reg_res2!=None:
                        nombre = reg_res2[1]
                        if len(nxt)%n==0:
                            num = int(len(nxt)/n)
                        else:
                            num = int(len(nxt)/n)+1
                        if with_numbers_jump_flag == True:
                            if nombre <= num:
                                return [True,message]
                            else:
                                return [False,message]
                        else:
                            if nombre == num:
                                return [True,message]
                            else:
                                return [False,message]
                    
            else:
                if message.strip().lower() == 'prev':
                    pass
                elif message.strip().lower() == 'next':
                    pass
                else:
                    nonefound_flag = True

    return None

