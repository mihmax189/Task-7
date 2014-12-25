#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import os
import re
#from requests import Request, Session
import requests
from lxml import html
from lxml import etree

class Request:
    def __init__(self):
        self.departure_str = ''
        self.distanation_str = ''
        self.outboun_date_str = ''
        self.return_date_str = ''
        self.one_way_str = ''

    def check_date(self, date_str):
        if not re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_str):
            print 'The date must be entered in the format yyyy-mm-dd'
            return 1
        # проверка на корректность значений года, месяца, дня
        date_components_list = date_str.split('-')
        error_flag = 0
        if int(date_components_list[0]) < 2014:
            print 'You have specified an incorrect year: ', date_components_list[0]
            error_flag = 1
        if int(date_components_list[1]) > 12:
            print 'You have specified an incorrect month: ', date_components_list[1]
            error_flag = 1
        if int(date_components_list[2]) > 31:
            print 'You have specified an incorrect number: ', date_components_list[2]
            error_flag = 1
        if error_flag:
            return 2

        return 0

    def get_parametrs(self):
        '''
        Метод получает от пользователя IATA-коды аэропортов отправления и назначения,
        даты вылета и прибытия. Если дата возрата не задается, то параметр 'в один конец'
        принимает значение 1.
        '''
        print 'Please enter the following values: '
        departure = distanation = outboun_date = return_date = ''

        while len(departure) == 0:
            departure = raw_input('IATA-code airport of departure (AAA): ')
            # look help(re)
            # описание строки шаблона '^[A-Z]$': введенная информация должна
            # состоять только из трех латинских символов в верхнем регистре
            if not re.match('^[A-Z]{3}$', departure):
                print 'IATA-code shell consist of three characters in uppercase'
                departure = ''
        while len(distanation) == 0:
            distanation  = raw_input('Arrival airport: ')
            if not re.match('^[A-Z]{3}$', distanation):
                print 'IATA-code shell consist of three characters in uppercase'
                distanation = ''

        while len(outboun_date) == 0:
            outboun_date = raw_input('Departure date (yyyy-mm-dd): ')
            if self.check_date(outboun_date):
                outboun_date = ''
                continue

        # дата возврата может быть и не введена
        return_date  = raw_input('Arrival date: ')
        # если пользователь ввел дату возврата, то проверяем ее на корректность
        incorrect_date = 1
        while incorrect_date:
            return_date  = raw_input('Arrival date: ')
            if self.check_date(return_date):
                return_date = ''
                continue
            incorrect_date = 0

        one_way = '0' if len(return_date) == 0 else '1'


def get_requests_post():
    url = 'http://www.flyniki.com/en-RU/start.php'
    info_requests = {
        'departure'   : 'DME',
        'destination' : 'PAR',
        'outbounDate' : '2014-12-26',
        'returnDate'  : '2014-12-26',
        'oneway'      : '1',
        'openDateOverview' : '0',
        'adulCount'   : '1',
        'childCount'  : '0',
        'infantCount' : '0'
    }

    with requests.session() as s:
        page = s.get(url)
        #r = s.post(url, data=info_requests)
        parsed_body = html.fromstring(page.text)
        print parsed_body.xpath('//title/text()')
        #print parsed_body.xpath('//a/@')
        print page.request.headers
    #return page

def parser(page):
    pass
    #returnDate = etree.xpath('//div[@class="floatRight"]/text()')
    #print 'Return date: ', returnDate
    #doc = html.document_fromstring(page)
    #p = etree.Element('http://www.flyniki.com/en-RU/start.php')
    #doc = etree.parse(page)

def write_to_file(res_text):
    output = open('result.txt', 'w')
    output.write(res_text)

def html_scraping(page):
    tree = html.fromstring(page.text)

def main():
    try:
        request = Request()
        request.get_parametrs()
        #get_requests_post()
        #parser(res)
    except requests.ConnectionError:
        print 'debug: Error http connection to www.flyniki.com!'
        exit(1)
    #except:
        #print 'debug: unknow error'
        #exit(1)

if __name__ == '__main__':
    main()
