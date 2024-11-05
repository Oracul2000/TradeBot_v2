import asyncio
import os
import json


allowed_users = [348691698, 540862463, 925216062]


async def newreports(bot):
    while True:
        await asyncio.sleep(1)
        reports = os.listdir('./bus/')
        for report in reports:
            d = {}
            with open('./bus/' + report, 'rt') as f:
                d = json.loads(f.read())
            for u in allowed_users:
                try:
                    if d['Type'] == 'PnL':
                        await bot.send_message(str(u), PnLReport(d))
                    if d['Type'] == 'TakeProfit':
                        await bot.send_message(str(u), TakeProfitReport(d))
                    if d['Type'] == 'Limit':
                        await bot.send_message(str(u), LimitReport(d))
                    else:
                        await bot.send_message(str(u), str(d))
                except:
                    pass
            os.remove('./bus/' + report)


def PnLReport(d):
    return f'Внимание! Отрицательный PnL!\nПользователь: {d["User Id"]}\nМонета: {d["symbol"]}\nPnL: {d["PnL"]}'
            

def LimitReport(d):
    return f'Внимание. Лимитный ордер восстановлен.\nПользователь: {d["User Id"]}\nМонета: {d["symbol"]}'


def TakeProfitReport(d):
    return f'Внимание. Take Profit ордер восстановлен.\nПользователь: {d["User Id"]}\nМонета: {d["symbol"]}'