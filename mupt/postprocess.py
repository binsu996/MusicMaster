import re

SEPARATORS = ['|', '|]', '||', '[|', '|:', ':|', '::']
SEP_DICT = {}
for i, sep in enumerate(SEPARATORS, start=1):
    # E.g. ' | ': ' <1>'
    SEP_DICT[' '+sep+' '] = f' <{i}>'
NEWSEP = '<|>'

def sep2tok(row):
    for sep, tok in SEP_DICT.items():
        row = row.replace(sep, tok+'<=> ')
    return row

def tok2sep(bar):
    for sep, tok in SEP_DICT.items():
        bar = bar.replace(tok, sep)
    return bar


def spacing(row):
    
    for sep in SEPARATORS:

        def subfunc(match):
            symbol = [':', '|', ']']
            if match.group(1) is None:
                return f' {sep}'
            elif match.group(1) in symbol:
                return f' {sep}{match.group(1)}'
            else:
                return ' '+sep+' '+match.group(1)
                
        pattern = r' ' + re.escape(sep) + r'(.{1})'
        row = re.sub(pattern, subfunc, row)
        row = row.replace('\n'+sep+'"', '\n '+sep+' "') # B \n|"A -> B \n | "A
        row = row.replace(' '+sep+'\n', ' '+sep+' \n')  # B |\n -> B | \n
    return row
  
def decode(piece):
    dec_piece = ''
    idx = piece.find(' '+NEWSEP+' ')
    heads = piece[:idx]
    scores = piece[idx:]
    scores_lst = re.split(' <\|>', scores)

    all_bar_lst = []
    for bar in scores_lst:
        if bar == '':
            continue
        bar = sep2tok(bar)
        bar_lst = re.split('<=>', bar)
        bar_lst = list(map(tok2sep, bar_lst))
        if len(all_bar_lst) == 0:
            all_bar_lst = [[] for _ in range(len(bar_lst))]
        for i in range(len(bar_lst)):
            all_bar_lst[i].append(bar_lst[i])

    if len(all_bar_lst) > 1:
        # There might be the bar number like %30 at the end 
        # which need to be specially handled.
        if len(all_bar_lst[0]) > len(all_bar_lst[1]):
            last_bar_lst = all_bar_lst[0][-1].split()
            all_bar_lst[0].pop()
            for i in range(len(all_bar_lst)):
                all_bar_lst[i].append(last_bar_lst[i])
                # Add the remaining symbols to the last row.
                if i == len(all_bar_lst) - 1:
                    for j in range(i+1, len(last_bar_lst)):
                        all_bar_lst[i][-1] += ' ' + last_bar_lst[j]
        # Ensure the lengths are consistent. 
        length = len(all_bar_lst[0])
        for lst in all_bar_lst[1:]:
            # assert len(lst) == length       
            pass

    dec_piece += heads
    for i in range(len(all_bar_lst)):
        if len(all_bar_lst) > 1:
            dec_piece += f'V:{i+1}\n'
        dec_piece += ''.join(all_bar_lst[i])
        dec_piece += '\n'
    # Remove redundant spaces.
    dec_piece = re.sub(' {2,}', ' ', dec_piece)

    return dec_piece