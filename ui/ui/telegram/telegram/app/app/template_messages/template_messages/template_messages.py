def useroutput(record):
    return f'''
#{record.id}#\t{record.name}'''

def userbigouput(record, ti):
    
    return f'''
Актуальный баланс: {round(ti.balance, 2)}USDT
Торговый депозит {record.symbol}USDT: {record.deposit} USDT
Api ключи: {ti.apiStatus}
Мониторинг:
{ti.monitoring()}\n'''

def apimonitoringoutput(record, ti):
    return f'\t{ti.monitoring().replace("Позиций: ", "").replace(", Ордеров: ", "").replace(", ТП: ", "")}'