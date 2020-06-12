#!/usr/local/bin/python3
# -*- coding: utf-8
import pickle
import os
import time

import re
import requests
from lxml import html

TOP_LEVEL_DOMAINS = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.arpa', '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bl', '.bm', '.bn', '.bo', '.bq', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', '.mf', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.ss', '.st', '.su', '.sv', '.sx', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', '.yt', '.za', '.zm', '.zw', 'الجزائر.', '.հայ', 'البحرين.', '.বাংলা', '.бел', '.бг[42]', '.中国', '.中國', 'مصر.', '.ею', '.გე', '.ελ[42]', '.香港', '.भारत', 'بھارت.', '.భారత్', '.ભારત', '.ਭਾਰਤ', '.இந்தியா', '.ভারত', '.ಭಾರತ', '.ഭാരതം', '.ভাৰত', '.ଭାରତ', 'بارت.', '.भारतम्', '.भारोत', 'ڀارت.', 'ایران.', 'عراق.', 'الاردن.', '.қаз', '.澳门', '.澳門', 'مليسيا.', 'موريتانيا.', '.мон', 'المغرب.', '.мкд', 'عمان.', 'پاکستان.', 'فلسطين.', 'قطر.', '.рф', 'السعودية.', '.срб', '.新加坡', '.சிங்கப்பூர்', '.한국', '.ලංකා', '.இலங்கை', 'سودان.', 'سورية.', '.台湾', '.台灣', '.ไทย', 'تونس.', '.укр', 'امارات.', 'اليمن.', '.academy', '.accountant', '.accountants', '.active', '.actor', '.ads', '.adult', '.aero', '.agency', '.airforce', '.analytics', '.apartments', '.app', '.archi', '.army', '.art', '.associates', '.attorney', '.auction', '.audible', '.audio', '.author', '.auto', '.autos', '.aws', '.baby', '.band', '.bank', '.bar', '.barefoot', '.bargains', '.baseball', '.basketball', '.beauty', '.beer', '.best', '.bestbuy', '.bet', '.bible', '.bid', '.bike', '.bingo', '.bio', '.biz', '.black', '.blackfriday', '.blockbuster', '.blog', '.blue', '.boo', '.book', '.boots', '.bot', '.boutique', '.box', '.broadway', '.broker', '.build', '.builders', '.business', '.buy', '.buzz', '.cab', '.cafe', '.call', '.cam', '.camera', '.camp', '.cancerresearch', '.capital', '.car', '.cards', '.care', '.career', '.careers', '.cars', '.case', '.cash', '.casino', '.catering', '.catholic', '.center', '.cern', '.ceo', '.cfd', '.channel', '.chat', '.cheap', '.christmas', '.church', '.cipriani', '.circle', '.city', '.claims', '.cleaning', '.click', '.clinic', '.clothing', '.cloud', '.club', '.coach', '.codes', '.coffee', '.college', '.community', '.company', '.compare', '.computer', '.condos', '.construction', '.consulting', '.contact', '.contractors', '.cooking', '.cool', '.coop', '.country', '.coupon', '.coupons', '.courses', '.credit', '.creditcard', '.cruise', '.cricket', '.cruises', '.dad', '.dance', '.data', '.date', '.dating', '.day', '.deal', '.deals', '.degree', '.delivery', '.democrat', '.dental', '.dentist', '.design', '.dev', '.diamonds', '.diet', '.digital', '.direct', '.directory', '.discount', '.diy', '.docs', '.doctor', '.dog', '.domains', '.dot', '.download', '.drive', '.duck', '.earth', '.eat', '.eco', '.education', '.email', '.energy', '.engineer', '.engineering', '.enterprises', '.equipment', '.esq', '.estate', '.events', '.exchange', '.expert', '.exposed', '.express', '.fail', '.faith', '.family', '.fan', '.fans', '.farm', '.fashion', '.fast', '.feedback', '.film', '.final', '.finance', '.financial', '.fire', '.fish', '.fishing', '.fit', '.fitness', '.flights', '.florist', '.flowers', '.fly', '.foo', '.food', '.foodnetwork', '.football', '.forsale', '.forum', '.foundation', '.free', '.frontdoor', '.fun', '.fund', '.furniture', '.fyi', '.gallery', '.game', '.games', '.garden', '.gdn', '.gift', '.gifts', '.gives', '.glass', '.global', '.gold', '.golf', '.gop', '.graphics', '.green', '.gripe', '.grocery', '.group', '.guide', '.guitars', '.guru', '.hair', '.hangout', '.health', '.healthcare', '.help', '.here', '.hiphop', '.hiv', '.hockey', '.holdings', '.holiday', '.homegoods', '.homes', '.homesense', '.horse', '.hospital', '.host', '.hosting', '.hot', '.hotels', '.house', '.how', '.ice', '.icu', '.industries', '.info', '.ing', '.ink', '.institute[75]', '.insurance', '.insure', '.international', '.investments', '.jewelry', '.jobs', '.joy', '.kim', '.kitchen', '.land', '.latino', '.law', '.lawyer', '.lease', '.legal', '.lgbt', '.life', '.lifeinsurance', '.lighting', '.like', '.limited', '.limo', '.link', '.live', '.living', '.loan', '.loans', '.locker', '.lol', '.lotto', '.love', '.ltd', '.luxury', '.makeup', '.management', '.map', '.market', '.marketing', '.markets', '.mba', '.med', '.media', '.meet', '.meme', '.memorial', '.men', '.menu', '.mint', '.mobi', '.mobile', '.mobily', '.moe', '.mom', '.money', '.mortgage', '.motorcycles', '.mov', '.movie', '.museum', '.music', '.name', '.navy', '.network', '.new', '.news', '.ngo', '.ninja', '.now', '.observer', '.off', '.one', '.ong', '.onl', '.online', '.ooo', '.open', '.organic', '.origins', '.page', '.partners', '.parts', '.party', '.pay', '.pet', '.pharmacy', '.phone', '.photo', '.photography', '.photos', '.physio', '.pics', '.pictures', '.pid', '.pin', '.pink', '.pizza', '.place', '.plumbing', '.plus', '.poker', '.porn', '.post', '.press', '.prime', '.pro', '.productions', '.prof', '.promo', '.properties', '.property', '.protection', '.pub', '.qpon', '.racing', '.radio', '.read', '.realestate', '.realtor', '.realty', '.recipes', '.red', '.rehab', '.reit', '.ren', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant', '.review', '.reviews', '.rich', '.rip', '.rocks', '.rodeo', '.room', '.rugby', '.run', '.safe', '.sale', '.save', '.scholarships', '.school', '.science', '.search', '.secure', '.security', '.select', '.services', '.sex', '.sexy', '.shoes', '.shop', '.shopping', '.show', '.showtime', '.silk', '.singles', '.site', '.ski', '.skin', '.sky', '.sling', '.smile', '.soccer', '.social', '.software', '.solar', '.solutions', '.song', '.space', '.spot', '.spreadbetting', '.storage', '.store', '.stream', '.studio', '.study', '.style', '.sucks', '.supplies', '.supply', '.support', '.surf', '.surgery', '.systems', '.talk', '.tattoo', '.tax', '.taxi', '.team', '.tech', '.technology', '.tel', '.tennis', '.theater', '.theatre', '.tickets', '.tips', '.tires', '.today', '.tools', '.top', '.tours', '.town', '.toys', '.trade', '.trading', '.training', '.travel', '.travelersinsurance', '.trust', '.tube', '.tunes', '.uconnect', '.university', '.vacations', '.ventures', '.vet', '.video', '.villas', '.vip', '.vision', '.vodka', '.vote', '.voting', '.voyage', '.wang', '.watch', '.watches', '.weather', '.webcam', '.website', '.wed', '.wedding', '.whoswho', '.wiki', '.win', '.wine', '.winners', '.work', '.works', '.world', '.wow', '.wtf', '.xxx', '.xyz', '.yachts', '.yoga', '.you', '.zero', '.zone', '.shouji', '.tushu', '.wanggou', '.weibo', '.xihuan', '.arte', '.clinique', '.luxe', '.maison', '.moi', '.rsvp', '.sarl', '.epost', '.gmbh', '.haus', '.immobilien', '.jetzt', '.kaufen', '.kinder', '.reise', '.reisen', '.schule', '.versicherung', '.desi', '.shiksha', '.casa', '.immo', '.moda', '.voto', '.bom', '.passagens', '.abogado', '.gratis', '.futbol', '.hoteles', '.juegos', '.ltda', '.soy', '.tienda', '.uno', '.viajes', '.vuelos', 'موقع.', '.كوم', '.موبايلي', '.كاثوليك', 'شبكة.', '.بيتك', 'بازار.', '.在线', '.中文网', '.网址', '.网站', '.网络', '.公司', '.商城', '.机构', '.我爱你', '.商标', '.世界', '.集团', '.慈善', '.八卦', '.公益', '.дети', '.католик', '.ком', '.онлайн', '.орг', '.сайт', '.संगठन', '.कॉम', '.नेट', '.닷컴', '.닷넷', '.קום\u200e', '.みんな', '.セール', '.ファッション', '.ストア', '.ポイント', '.クラウド', '.コム', '.คอม', '.africa', '.capetown', '.durban', '.joburg', '.abudhabi', '.arab', '.asia', '.doha', '.dubai', '.krd', '.kyoto', '.nagoya', '.okinawa', '.osaka', '.ryukyu', '.taipei', '.tatar', '.tokyo', '.yokohama', '.alsace', '.amsterdam', '.bcn', '.barcelona', '.bayern', '.berlin', '.brussels', '.budapest', '.bzh', '.cat', '.cologne', '.corsica', '.cymru', '.eus', '.frl', '.gal', '.gent', '.hamburg', '.helsinki', '.irish', '.ist', '.istanbul', '.koeln', '.london', '.madrid', '.moscow\xa0[ru]', '.nrw', '.paris', '.ruhr', '.saarland', '.scot', '.stockholm', '.swiss', '.tirol', '.vlaanderen', '.wales', '.wien', '.zuerich', '.boston', '.miami', '.nyc', '.quebec', '.vegas', '.kiwi', '.melbourne', '.sydney', '.lat', '.rio', '.佛山', '.广东', '.москва\xa0[ru]', '.рус\xa0[ru]', '.ابوظبي', '.عرب', '.aaa', '.aarp', '.abarth', '.abb', '.abbott', '.abbvie', '.abc', '.accenture', '.aco', '.aeg', '.aetna', '.afl', '.agakhan', '.aig', '.aigo', '.airbus', '.airtel', '.akdn', '.alfaromeo', '.alibaba', '.alipay', '.allfinanz', '.allstate', '.ally', '.alstom', '.americanexpress', '.amex', '.amica', '.android', '.anz', '.aol', '.apple', '.aquarelle', '.aramco', '.audi', '.auspost', '.axa', '.azure', '.baidu', '.bananarepublic', '.barclaycard', '.barclays', '.basketball', '.bauhaus', '.bbc', '.bbt', '.bbva', '.bcg', '.bentley', '.bharti', '.bing', '.blanco', '.bloomberg', '.bms', '.bmw', '.bnl', '.bnpparibas', '.boehringer', '.bond', '.booking', '.bosch', '.bostik', '.bradesco', '.bridgestone', '.brother', '.bugatti', '.cal', '.calvinklein', '.canon', '.capitalone', '.caravan', '.cartier', '.cba', '.cbn', '.cbre', '.cbs', '.cern', '.cfa', '.chanel', '.chase', '.chintai', '.chrome', '.chrysler', '.cisco', '.citadel', '.citi', '.citic', '.clubmed', '.comcast', '.commbank', '.creditunion', '.crown', '.crs', '.csc', '.cuisinella', '.dabur', '.datsun', '.dealer', '.dell', '.deloitte', '.delta', '.dhl', '.discover', '.dish', '.dnp', '.dodge', '.dunlop', '.dupont', '.dvag', '.edeka', '.emerck', '.epson', '.ericsson', '.erni', '.esurance', '.etisalat', '.eurovision', '.everbank', '.extraspace', '.fage', '.fairwinds', '.farmers', '.fedex', '.ferrari', '.ferrero', '.fiat', '.fidelity', '.firestone', '.firmdale', '.flickr', '.flir', '.flsmidth', '.ford', '.fox', '.fresenius', '.forex', '.frogans', '.frontier', '.fujitsu', '.fujixerox', '.gallo', '.gallup', '.gap', '.gbiz', '.gea', '.genting', '.giving', '.gle', '.globo', '.gmail', '.gmo', '.gmx', '.godaddy', '.goldpoint', '.goodyear', '.goog', '.google', '.grainger', '.guardian', '.gucci', '.hbo', '.hdfc', '.hdfcbank', '.hermes', '.hisamitsu', '.hitachi', '.hkt', '.honda', '.honeywell', '.hotmail', '.hsbc', '.hughes', '.hyatt', '.hyundai', '.ibm', '.ieee', '.ifm', '.ikano', '.imdb', '.infiniti', '.intel', '.intuit', '.ipiranga', '.iselect', '.itau', '.itv', '.iveco', '.jaguar', '.java', '.jcb', '.jcp', '.jeep', '.jpmorgan', '.juniper', '.kddi', '.kerryhotels', '.kerrylogistics', '.kerryproperties', '.kfh', '.kia', '.kinder', '.kindle', '.komatsu', '.kpmg', '.kred', '.kuokgroup', '.lacaixa', '.ladbrokes', '.lamborghini', '.lancaster', '.lancia', '.lancome', '.landrover', '.lanxess', '.lasalle', '.latrobe', '.lds', '.lego', '.liaison', '.lexus', '.lidl', '.lifestyle', '.lilly', '.lincoln', '.linde', '.lipsy', '.lixil', '.locus', '.lotte', '.lpl', '.lplfinancial', '.lundbeck', '.lupin', '.macys', '.maif', '.man', '.mango', '.marriott', '.maserati', '.mattel', '.mckinsey', '.metlife', '.microsoft', '.mini', '.mit', '.mitsubishi', '.mlb', '.mma', '.monash', '.mormon', '.moto', '.movistar', '.msd', '.mtn', '.mtr', '.mutual', '.nadex', '.nationwide', '.natura', '.nba', '.nec', '.netflix', '.neustar', '.newholland', '.nexus', '.nfl', '.nhk', '.nico', '.nike', '.nikon', '.nissan', '.nissay', '.nokia', '.northwesternmutual', '.norton', '.nra', '.ntt', '.obi', '.office', '.omega', '.oracle', '.orange', '.otsuka', '.ovh', '.panasonic', '.pccw', '.pfizer', '.philips', '.piaget', '.pictet', '.ping', '.pioneer', '.play', '.playstation', '.pohl', '.politie', '.praxi', '.prod', '.progressive', '.pru', '.prudential', '.pwc', '.quest', '.qvc', '.redstone', '.reliance', '.rexroth', '.ricoh', '.rmit', '.rocher', '.rogers', '.rwe', '.safety', '.sakura', '.samsung', '.sandvik', '.sandvikcoromant', '.sanofi', '.sap', '.saxo', '.sbi', '.sbs', '.sca', '.scb', '.schaeffler', '.schmidt', '.schwarz', '.scjohnson', '.scor', '.seat', '.sener', '.ses', '.sew', '.seven', '.sfr', '.seek', '.shangrila', '.sharp', '.shaw', '.shell', '.shriram', '.sina', '.sky', '.skype', '.smart', '.sncf', '.softbank', '.sohu', '.sony', '.spiegel', '.stada', '.staples', '.star', '.starhub', '.statebank', '.statefarm', '.statoil', '.stc', '.stcgroup', '.suzuki', '.swatch', '.swiftcover', '.symantec', '.taobao', '.target', '.tatamotors', '.tdk', '.telecity', '.telefonica', '.temasek', '.teva', '.tiffany', '.tjx', '.toray', '.toshiba', '.total', '.toyota', '.travelchannel', '.travelers', '.tui', '.tvs', '.ubs', '.unicom', '.uol', '.ups', '.vanguard', '.verisign', '.vig', '.viking', '.virgin', '.visa', '.vista', '.vistaprint', '.vivo', '.volkswagen', '.volvo', '.walmart', '.walter', '.weatherchannel', '.weber', '.weir', '.williamhill', '.windows', '.wme', '.wolterskluwer', '.woodside', '.wtc', '.xbox', '.xerox', '.xfinity', '.yahoo', '.yamaxun', '.yandex', '.yodobashi', '.youtube', '.zappos', '.zara', '.zip', '.zippo', '.ارامكو', '.اتصالات', '.联通', '.移动', '.中信', '.香格里拉', '.淡马锡', '.大众汽车', '.vermögensberater', '.vermögensberatung', '.グーグル', '.谷歌', '.工行', '.嘉里', '.嘉里大酒店', '.飞利浦', '.诺基亚', '.電訊盈科', '.삼성', '.example', '.invalid', '.local', '.localhost', '.onion', '.test']


class ExtractEmails:
    """
    Extract emails from a given website
    """

    def __init__(self, url: str, depth: int=None, print_log: bool=False, ssl_verify: bool=True, user_agent: str=None, request_delay: float=0, cookies: dict = None):
        self.delay = request_delay
        self.verify = ssl_verify
        if url.endswith('/'):
            self.url = url[:-1]
        else:
            self.url = url
        self.print_log = print_log
        self.depth = depth
        self.scanned = []
        self.for_scan = []
        self.emails = []
        self.headers = {'User-Agent': user_agent}
        self.extract_emails(url)
        self.cookies = cookies

    def extract_emails(self, url):
        r = requests.get(url, headers=self.headers, verify=self.verify, cookies=self.cookies)
        self.scanned.append(url)
        if r.status_code == 200:
            self.get_all_links(r.content)
            self.get_emails(r.text)
        if self.print_log:
            self.print_logs()
        for new_url in self.for_scan[:self.depth]:
            if new_url not in self.scanned:
                time.sleep(self.delay)
                self.extract_emails(new_url)

    def print_logs(self):
        print('URLs: {}, emails: {}'
              .format(len(self.scanned), len(self.emails)))

    def get_emails(self, page):
        emails = re.findall(r'\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b', page)
        emails = [x.lower() for x in emails]
        emails = [x for x in emails if '.' + x.split('.')[-1] in TOP_LEVEL_DOMAINS]
        if emails:
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)

    def get_all_links(self, page):
        try:
            tree = html.fromstring(page)
        except ValueError:
            tree = None
        if tree is not None:
            all_links = tree.findall('.//a')
            for link in all_links:
                try:
                    link_href = link.attrib['href']
                    check_href_url = re.sub(r'https?://', '', link_href)
                    check_self_url = re.sub(r'https?://', '', self.url)
                    if check_href_url.startswith(check_self_url) or check_href_url.startswith('/'):
                        if check_href_url.startswith('/'):
                            link_href = self.url + link_href
                        if check_href_url not in self.for_scan:
                            self.for_scan.append(link_href)
                except KeyError:
                    pass


if __name__ == '__main__':
    em = ExtractEmails('http://www.ThreeVillagePodiatry.com', print_log=True, user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
                       depth=10)
    print(em.emails)
