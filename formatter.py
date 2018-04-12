def make_table(table):
    csv = []
    for row in table:
        row_data = []
        for cell in row:
            temp = cell.data.replace(',','.').replace('|', '!')
            temp = ' {} '.format(temp)
            row_data.append(temp)
        csv.append(','.join(row_data))
    max_len = 0
    
    for row in csv:
        x = len(row.split(','))
        if x > max_len:
            max_len = x
    
    header = ''
    if len(csv[0].split(',')) < max_len:
        header = str(csv[0])
        csv = csv[1:]
    
    csv.insert(1, '|'.join([':--']*max_len))
    csv[0] = csv[0].replace(' ', '.')
    csv = '\n'.join(csv)
    csv = csv.replace(',', '|')
    return header +'\n\n' + csv

def to_reddit_table(model):
    tables = model.summary().tables
    text = ''
    for table in tables:
        text = text +   ' \n\n __  \n\n  ' + make_table(table)
    return text
