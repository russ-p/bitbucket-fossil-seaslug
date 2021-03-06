# -*- coding: utf-8 -*-
"""
Created on 29.03.2011

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import random

from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur

def chat_response(f):
    "decorator"
    def wrp(self, botMessage):
#            func_doc = f.func_doc
        param = f (self, botMessage)
        if len(botMessage.params) > 0:
            name = botMessage.paramString
        else:
            name = botMessage.sender.name
        botMessage.send_response ( ru('/me %s %s %s %s') % (random.choice(param[0]), random.choice(param[1]),random.choice(param[2]), name))
    wrp.func_doc = f.func_doc
    return wrp

class BarPlugin(Plugin):
    # откуда вытаскивать
    bar_find = [ru("достал из холодильника"),
                ru("вытащил из холодильника"),
                ru("достал из бара"),
                ru("вытащил из бара"),
                ru("взял с полки"),
                ru("взял со стола"),
                ru("принес из магазина"),
                ru("вытащил из тумбочки"),
                ru("купил")]

    bar_find_wine = [
        ru("достал из бара"),
        ru("вытащил из бара"),
        ru("взял с полки"),
        ru("взял со стола"),
        ru("достал из погреба"),
        ru("достал из погребка"),
        ru("принес из магазина"),
        ru("вытащил из тумбочки"),
        ru("купил")]
    
# метод перидачи напитков
    bar_put = [
        ru("и дрожащими руками, отдал"),
        ru("и дрожащими руками, протянул"),
        ru("и дрожащими руками, передал"),
        ru("и передал"),
        ru("и всхлипнув, передал"),
        ru("и протянул"),
        ru("и передал")]

    bar_drink_beer = [
        ru("бутылочку пива 'Старый Мельник'"),
        ru("бутылку пива 'Старый Мельник'"),
        ru("банку пива 'Старый Мельник'"),
        ru("бутылочку пива 'LowenBrau'"),
        ru("бутылку пива 'LowenBrau'"),
        ru("банку пива 'LowenBrau'"),
        ru("бутылочку пива 'Солодов'"),
        ru("бутылку пива 'Солодов'"),
        ru("банку пива 'Солодов'"),
        ru("бутылочку пива 'Доктор Дизель'"),
        ru("бутылку пива 'Доктор Дизель'"),
        ru("банку пива 'Доктор Дизель'"),
        ru("бутылочку пива 'Невское'"),
        ru("бутылку пива 'Невское'"),
        ru("банку пива 'Невское'"),
        ru("бутылочку пива 'Три Богатыря'"),
        ru("бутылку пива 'Три Богатыря'"),
        ru("банку пива 'Три Богатыря'"),
        ru("бутылочку пива 'Сибирская Корона'"),
        ru("бутылку пива 'Сибирская Корона'"),
        ru("банку пива 'Сибирская Корона'"),
        ru("бутылочку пива 'Белый Медведь'"),
        ru("бутылку пива 'Белый Медведь'"),
        ru("банку пива 'Белый Медведь'"),
        ru("бутылочку пива 'Клинское'"),
        ru("бутылку пива 'Клинское'"),
        ru("банку пива 'Клинское'"),
        ru("бутылочку пива 'Пит'"),
        ru("бутылку пива 'Пит'"),
        ru("банку пива 'Пит'"),
        ru("бутылочку пива 'EFES Pilsner'"),
        ru("бутылку пива 'EFES Pilsner'"),
        ru("банку пива 'EFES Pilsner'"),
        ru("бутылочку пива 'Клинское REDKOE'"),
        ru("бутылку пива 'Клинское REDKOE'"),
        ru("банку пива 'Клинское REDKOE'"),
        ru("бутылочку пива 'Клинское Самурай'"),
        ru("бутылочку пива 'Будвайзер'"),
        ru("бутылку пива 'Будвайзер'"),
        ru("банку пива 'Будвайзер'"),
        ru("бутылочку пива 'Балтика'"),
        ru("бутылку пива 'Балтика'"),
        ru("банку пива 'Балтика'"),
        ru("бутылочку пива 'Бочкарев'"),
        ru("бутылку пива 'Бочкарев'"),
        ru("банку пива 'Бочкарев'"),
        ru("бутылочку пива 'Золотая Бочка'"),
        ru("бутылку пива 'Золотая Бочка'"),
        ru("банку пива 'Золотая Бочка'"),
        ru("бутылочку пива 'Tinkoff'"),
        ru("бутылку пива 'Tinkoff'"),
        ru("банку пива 'Tinkoff'")]

    bar_drink_vodka = [
        ru("бутылку водки 'Гжелка', налил рюмаху"),
        ru("бутылку водки 'Русский Размер', плеснул рюмаху"),
        ru("бутылку водки 'Флагман', налил в румочку"),
        ru("бутылку водки 'Смирнофф', налил в рюмку"),
        ru("бутылку водки 'Арбатская', налил в граненый стакан"),
        ru("бутылку водки 'Кристалл', налил в рюмаху"),
        ru("бутылку водки 'Юрий Долгорукий', плеснул в рюмаху"),
        ru("бутылку водки 'Абсолют', аккуратненько налил в рюмочку,"),
        ru("бутылку водки 'Парламент', налил в рюмку"),
        ru("бутылку водки 'Русский размер', плеснул в рюмку"),
        ru("пузырь водяры, плеснул в рюмку"),
        ru("банку самогона, ливанул в рюмку")]

    bar_drink_water = [
        ru("бутылочку воды 'Аква Минерале', налил в стакан"),
        ru("пол литровую бутылочку воды 'Бон Аква'"),
        ru("воду 'Ессентуки'"),
        ru("кувшин с водой 'Нарзан', налил в бокал"),
        ru("бутылку воды 'Шишкин лес'"),
        ru("литровую бутылку воды 'Валдай', налил в стакан"),
        ru("воду 'Святой источник', налил в кружку"),
        ru("бутылку воды 'Сенежская', налил в кружку"),
        ru("бутылочку водички 'Перье', аккуратненько налил в бокал"),
        ru("воду 'Архыз', плеснул в стакан"),
        ru("баночку воды 'Pepsi'"),
        ru("бутылочку воды 'Coca-Cola'"),
        ru("бутылку воды 'Pepsi', налил в стакан"),
        ru("бутылку воды 'Coca-Cola', аккуратно налил в стакан"),
        ru("баночку 'Sprite'"),
        ru("литровую бутылку воды '7 UP', налил в стакан"),
        ru("воды 'Fanta', налил в бокал")]

    bar_drink_coctail = [
        ru("коктейль 'Казанова Дыня'"),
        ru("баночку коктейля'Казанова'"),
        ru("банку коктейля 'Трофи Фейхоа'"),
        ru("коктейл 'Трофи Дыня'"),
        ru("баночку коктейля 'Трофи'"),
        ru("коктейль 'МАГДАЛИНА'"),
        ru("коктейль 'отвертка'"),
        ru("банку коктейля 'отвертка'"),
        ru("коктейль 'Bravo'")]

    bar_drink_wine = [
        ru("бутылку вина 'Арбатское', налил бокал"),
        ru("бутылку вина 'Изабелла', осторожно налил бокал"),
        ru("вино 'Кагор', аккуратно налил бокал"),
        ru("бутылку вина 'Кровь Драконa', налил бакал"),
        ru("вино 'Каберне Крымское', налил бокал"),
        ru("бутылку вина 'Малезан Божоле', аккуратно налил бокал"),
        ru("вино 'Малезан Бордо', налил бокал"),
        ru("бутылку вина 'Бовийон Бордо', осторожно налил бокальчик"),
        ru("вино 'Кюве Дю Пап', налил бокал"),
        ru("бутылку вина 'Листель Мерло', осторожно открыл, налил бокал")]

    bar_drink_coffee = [
        ru("банку 'Nescafe', вскипятил чайник, приготовил чашечку кофе"),
        ru("банку 'Nescafe', приготовил чашечку ароматного кофе"),
        ru("банку кофе 'Jacobs', приготовил чашку"),
        ru("кофе 'Chibo', приготовил"),
        ru("'Маккофе', заварил чашечку")]

    bar_drink_juice = [
        ru("пачку сока 'Sokos', налил в стакан"),
        ru("сок 'J-7', аккуратно налил в стакан"),
        ru("Апельсиновый сок"),
        ru("пачку Апельсинового сока, налил в стакан"),
        ru("пачку сока 'Добрый', осторожно налил в бокал"),
        ru("пачку сока 'Gold Premium', налил в стакан"),
        ru("сок 'Gold Premium'"),
        ru("Ананасовй сок, налил в стаканчик"),
        ru("сок 'Любимый Сад', налил в стакан"),
        ru("сок 'Rich', налил в стакан"),
        ru("сок 'Rich', аккуратно налил в стакан")]

    bar_drink_kon = [
        ru("коньяк 'Арарат', плеснул рюмку"),
        ru("бутылку коньяка 'Арарат', аккуратно налил рюмку"),
        ru("коньяк 'Московский', налил рюмаху"),
        ru("коньяк 'Арбатский', осторожно налил рюмаху"),
        ru("бутылку коньяка 'Арбатский', налил рюмку"),
        ru("бутылку коньяка 'Кремлевский', неспеша налил рюмку "),
        ru("коньяк 'Бастион', налил рюмочку"),
        ru("бутылку коньяка 'Курвуазье', аккуратно налил рюмку")]

    bar_drink_shampun = [
        ru("шампанское 'Крымское', налил фужер"),
        ru("'Советское' шампанское, аккуратно налил фужер"),
        ru("бутылку шампанского 'Корнет', налил фужер"),
        ru("шампанское 'Одесса', осторожно налил фужер"),
        ru("бутылку 'Асти Мондоро', неспеша налил фужер"),
        ru("шампанское 'Вдова Клико', налил фужер")]

    bar_drink_tee = [
        ru("чай 'Lipton', заварил кружечку"),
        ru("чай 'Беседа', заварил кружку"),
        ru("чай 'Ахмад', заварил в кружке"),
        ru("чай 'Милфорд', заварил кружку"),
        ru("'Майский' чай, заварил")]
    
    plugin_name = 'bar'
    
    def init(self):
        # Команды:
        #    !бар
        #    !пиво
        #    !водка
        #    !коньяк
        #    !коктейл
        #    !вино
        #    !шампанское
        #    !кофе
        #    !чай
        #    !сок
        #    !вода
        self.commands = {
        ru('!пиво') :  self.beer ,
        ru('!водка') :  self.vodka,
        ru('!коньяк') :  self.koniak,
        ru('!коктейл') :  self.kokteil,
        ru('!вино') :  self.vino,
        ru('!шампанское') :  self.shampanskoe,
        ru('!кофе') : self.coffee,
       #ru('!чай')] : self.tee,
        ru('!сок') :  self.sok,
        ru('!вода') : self.water}   
       
    @chat_response
    def vodka(self, botMessage):
        """Угостить водкой"""
        return (self.bar_find, self.bar_drink_vodka, self.bar_put)
    
    @chat_response        
    def beer(self, n):
        """Угостить пивом"""
        return (self.bar_find, self.bar_put, self.bar_drink_beer) 
    
    @chat_response    
    def water(self, name):
        """Угостить напитком"""
        return (self.bar_find, self.bar_drink_water, self.bar_put)
    
    @chat_response
    def kokteil(self, name):
        """Угостить коктелем"""
        return (self.bar_find, self.bar_drink_coctail, self.bar_put)
    
    @chat_response
    def vino(self, name):
        """Угостить вином"""
        return (self.bar_find_wine, self.bar_drink_wine, self.bar_put)
    
    @chat_response
    def coffee(self, name):
        """Угостить кофе"""
        return (self.bar_find, self.bar_drink_coffee, self.bar_put)  
    
    @chat_response
    def sok(self, name):
        """Угостить соком"""
        return (self.bar_find, self.bar_drink_juice, self.bar_put) 
    
    @chat_response
    def koniak(self, name):
        """Угостить коньяком"""
        return (self.bar_find, self.bar_drink_kon, self.bar_put) 
    
    @chat_response
    def shampanskoe(self, name):
        """Угостить """
        return (self.bar_find, self.bar_drink_shampun, self.bar_put)        
   
if __name__ == '__main__':
    b = BarPlugin().test_commands()
