# coding=utf-8
# !/usr/bin/python

import re

import PyMysql

import common.DbUtil as DbUtil


def subtract_three_month(member_list):
    failed_count = 0
    success_count = 0
    sql = " UPDATE sibu_directsale_profit_{module}.member_deal d SET d.apply_date = DATE_ADD(d.apply_date,  INTERVAL - 3 MONTH ), d.offset_flag = 3  WHERE " \
          " d.apply_month = {profit_month} AND d.apply_money = {apply_money}*100  AND d.apply_member_id = '{member_id}' AND d.deal_status =4"
    for i in member_list:
        apply_money = i[2]
        profit_month = i[1]
        member_id = i[0]
        module = DbUtil.get_mod_16(member_id)
        db = PyMysql.connect("10.47.32.108", "sibu_dbuser", "TY3WxTv9CIiOtefN", "sibu_directsale")
        cursor = db.cursor()
        cursor.execute(sql.format(module=module, profit_month=profit_month, apply_money=apply_money, member_id=member_id))
        try:
            db.commit()
            success_count += 1
            print("successCount: " + str(success_count))
        except:
            failed_count += 1
            print("failed: " + str(member_id) + " count:" + str(failed_count))
            db.rollback()
        db.close()


def add_three_month(member_list):
    failed_count = 0
    success_count = 0
    sql = " UPDATE sibu_directsale_profit_{module}.member_deal d SET d.apply_date = DATE_ADD(d.apply_date,  INTERVAL 3 MONTH ) WHERE d.apply_month = {profit_month} " \
          "AND d.apply_money = {apply_money}*100 AND d.apply_member_id = '{member_id}' AND d.deal_status = 8"
    for i in member_list:
        apply_money = i[2]
        profit_month = i[1]
        member_id = i[0]
        module = DbUtil.get_mod_16(member_id)
        db = PyMysql.connect("10.47.32.108", "sibu_dbuser", "TY3WxTv9CIiOtefN", "sibu_directsale")
        cursor = db.cursor()
        cursor.execute(sql.format(module=module, profit_month=profit_month, apply_money=apply_money, member_id=member_id))
        try:
            db.commit()
            success_count += 1
            print("successCount: " + str(success_count))
        except:
            failed_count += 1
            print("failed: " + member_id + " count:" + str(failed_count))
            db.rollback()
        db.close()

def get_member_id(phone_list):
    db = PyMysql.connect("10.47.32.108", "sibu_dbuser", "TY3WxTv9CIiOtefN", "sibu_directsale")
    cursor = db.cursor()
    for i in phone_list:
        i = str(i).strip()
        a = re.findall(r'(\w*[0-9]+)\w*', i)
        cursor.execute("select member_id from sibu_directsale.member WHERE phone =%s"% (a[0]));
        result = cursor.fetchone()
        print(result[0])

deal_list = [
('b616a29394f54e0d9a481c1943dca6c7','201607',78.85),
('0659df494c794d8f9adbe5497969bec8','201607',96),
('4bc507f63cc0476da69cc528cd344c22','201607',99),
('60dafa1c2bf14e02969ab58a53c27f56','201607',165),
('b4fcad51fb66496c9d1a6a34ed8d0611','201606',184),
('cdca53a8a4a8467b936ae11df8020c1c','201608',198.29),
('27828c156a5b4a2780f2e4b44f87722d','201608',231),
('afe735d3840e4b0db20e4695491cd2b1','201607',569.88),
('3e9321fef61b41d0878f7c511433c248','201607',252.76),
('26151c95091e490893adedc5efe9aaa5','201608',693.15),
('2dd6e0e73a2f4fd4ae861ee0a17830d2','201607',914),
('34b453e5ad364813bd44d4d4ace073ad','201607',952.34),
('afe735d3840e4b0db20e4695491cd2b1','201607',976),
('f7d9cd63142f433886073d8add1cf4f1','201607',2000),
('c93e1e8975f746f7ab5998397d57eb29','201607',864),
('e349ce67612a4269a22b026d95485247','201606',923),
('9b0b31c9676a4f7db1c63e60446f16e9','201607',3303.95),
('0ddc4c3601b14b26aadfe5f7e638b5dd','201608',3512),
('0fd09c54fd7c48b0873e2022dba1fa42','201607',3524.53),
('b7e6a3008833408aae31affe08c8da52','201607',3535),
('f793f4f5b0804a1bab0bc00bfeac9bca','201606',3540),
('2dd6e0e73a2f4fd4ae861ee0a17830d2','201607',1500),
('a57c77cd2f6d420e961ac3cea09933bf','201607',3569.82),
('60dafa1c2bf14e02969ab58a53c27f56','201607',3030),
('9d98301f6c65418d9cf9e0d7ac40b0ab','201606',3586),
('afe09c3ceffb4b01924a43b25a38f3ef','201607',985.36),
('2117926d71674969a3cf80a7f6258c98','201607',1800),
('b84db8671b94465c9ddd03b8e6853c1b','201606',600),
('ca0a06cba4854ee8b6030cd5ad2779f4','201606',2540.75),
('1670f39666954f85897653f34c8adfdf','201607',2722.61),
('a48ce642427d4a64934b78527170cf67','201608',3618),
('4b8a134bbc994b63aba35217f8d69acd','201608',3619.32),
('ecfb3274c37e49dca2e6e4814c78441a','201608',3646.5),
('7ba66889c87f44c68d9f39c132f546a9','201608',3662),
('f7a8851072ff42afaf9b73abe423829b','201608',3400),
('f7a8851072ff42afaf9b73abe423829b','201608',3674.25),
('4a43a76bb44e4703aad449773ffd21d3','201608',1009),
('13749534aa8c487abf5e9c085045e31d','201607',3499),
('a75a95fc84194b4b9c0b24ea3742e6e8','201607',1095),
('615ee6e4501a4e49acd4b9e9124b4151','201607',388),
('e6b5b2948b97445e8936d4b58084b0da','201608',1251),
('e53a0fb17cb144a3967dcd359880394f','201606',769.27),
('96354694c4814900a84e5cbb5f163117','201607',450),
('26151c95091e490893adedc5efe9aaa5','201608',988),
('7eddf2a20a2f4980b62ce5ba9f3b677b','201607',666),
('cf50c7ba18dc4a07b147240f1021ac85','201608',1134),
('4bc507f63cc0476da69cc528cd344c22','201607',3870.94),
('8a13eea8e81a4555bc529240d1eb5419','201606',578),
('652a0c48c2df492a8c5f8c8ad334b054','201606',3884),
('d34a26c06efc4d45b17747f7d76552e5','201606',400),
('7ccd9b8a9a8b408d9d96eb9f183b48bf','201606',3900),
('c09a5525dada451a9902ffeda437843c','201607',3056),
('4a6ff534d98d4ad08df5e771e35bb62f','201607',550.55),
('b4433c5174df4d44a942c1dfbe33bfc5','201607',3558.27),
('4cdd8b22dd59450f84fe56bc18f8f49c','201606',4000),
('179d1c37512e4ec99ec79101b4d5a94e','201605',4000),
('27828c156a5b4a2780f2e4b44f87722d','201608',548),
('a8e5817440304560a1eeffe8d97f49a3','201606',4054.91),
('d3d2a3171c054c3cb4ea0465c5cbc9c0','201607',566.9),
('47f5f620873042a7a5ff1056e6732ad9','201607',606),
('bb643ab1f8f44d05aa90aa3d7b32cf7b','201607',4073.25),
('1eeb250068f74451a152d8334c85d6c5','201607',1084),
('717fcc5c15e74eef9df4911165e06bed','201606',3535),
('3df2414290d94c2cbec3bad68b7d94e8','201607',800),
('01f0e02cadb0465da5f79ae2932106bb','201607',4100),
('bfecfcafd09d4a1a9fe7bbc81e098967','201607',962),
('a2afd01e71a14dfd90aea31b20d2eddd','201607',4112),
('b4fcad51fb66496c9d1a6a34ed8d0611','201606',1119),
('e8aa6b2d0b7b4cb48710a10081c13240','201606',2124.91),
('b52b00d15d0a437eb9e6ae1757c23444','201607',2651),
('3519114cfdea46c8a3f084003f087c0f','201608',4138),
('e9b23597914f4b8d9da3c7dc779744bb','201606',4177.26),
('d303a5fbcf0a41a8831d807ad50f5568','201608',4179.19),
('4fccdf87c7154a779cc096b780265bad','201607',732),
('680c60bccee4409e8f5765defe880620','201607',1000),
('6d614c8c142c49cbac92838f73bbfa10','201606',4400),
('416a3a4213df49ae98b58880a9d16b27','201607',4400),
('17a1f690b5dc4286bcda0899c18b52f8','201607',4400),
('5820b96ee34a4179b20705e93d3861be','201608',1423),
('34b453e5ad364813bd44d4d4ace073ad','201607',1545.15),
('a69a15709e7147aa8218dd5c0fc0f5a3','201607',1038),
('6b3a70d9779848b8835dd685e563a12e','201608',4518),
('f7d9cd63142f433886073d8add1cf4f1','201607',1566),
('132f451837f5443a84ee3f9b5b7e1060','201607',4600),
('0a206fff17524d818bae8a46dd5957cc','201607',4615.29),
('e3dfbdce7eb54e6d980193d640aece11','201607',4657),
('d14fb7e65825419f97531fcef8316562','201607',2923),
('f0d726eba3424e37bbb985fdda643825','201607',1205.67),
('ccf956f7166a4ec0b6befef69ea3c328','201607',1452.85),
('2909c4e882664795bdde0f7aff062a80','201608',4750),
('b6d89434bb964125b765a3cfe4fa58ba','201607',4824.59),
('e102d8b51504402686893598941af944','201607',3536),
('1110b89c01ed4f4eafd049ac1a99bcd4','201606',4968),
('2dcad62e0df54918a40c6050be1c4967','201607',1970),
('332baaae8eda4a248702e6b3972461f6','201607',2370),
('2b1f911d7e50454db4b7367746855a07','201607',1823.5),
('7bc631af3a004b58ae5a9d5df2b3cc4d','201607',5071),
('ffc7c81e058c4a87b9879d4633fd3523','201607',5156.25),
('487190988d654ae291e8839284ebb953','201608',5372.92),
('f9ae4b0c12c24b9293277a542bd94c48','201606',1983.69),
('bf31cfceb435483ebd36e5be0d2322bd','201607',4555),
('f7a41796dc2a4a59a486fb3b78664cef','201608',5731.05),
('4faf42228dda4e588ec458de091489cb','201607',3484.85),
('00e6f19e66584e489fa804fcb9849398','201606',5880),
('7f4384af42bc496fa356e462ac606825','201607',2422.11),
('cabc064891fe4547b8bdd47091a5ec4f','201607',5933),
('ad3ac16086f348ecabe57c2ca92254c6','201606',6015),
('1170abc28e394808a9902fbae77b2f00','201608',6170),
('77313e6781944cf584035f1178f5b774','201607',2674),
('52d0e4eca43b4cd2aa72626988bfbe46','201607',2683),
('85cbe26b986948b19fcacb28612df091','201607',2900),
('bfcadb23f84f49b8a04113385934a636','201607',2946),
('dd04b022b83b437ea0273a309f5db026','201607',2867),
('4c935dbbbdcf470d82636cf495f50ade','201607',2896.31),
('83a274c3c73546ec8232253d1fd28912','201608',2898.71),
('6f65b5a2f8354c4083cfb1b37f6b316c','201606',3019.5),
('7ec827a1bad04a929406facfefd150ab','201607',3713),
# ('d8c7ad79d3df49fe9683c1f595ae8fd8','201608',3209),
('89b89872a5c745e993f018294d159f6b','201606',3311),
('e2089737c56d4eecb00d3bdba6ae3350','201607',3260.47),
('3667290da9a641a2be668abdd82e6cd8','201607',3299.68),
('de5c01126e1e42399e002409c0512db2','201608',3341.31),
('46f13cc6a9d64c22a34b2f2d87d98e13','201606',3500),
('46f13cc6a9d64c22a34b2f2d87d98e13','201606',3500),
('dd90d2d11b6341b59ddec55d62deba25','201607',3500),
('896963ad5a2648b3a89cb07e2fd302c0','201608',7378),
('3422041ef9a543268f62a2bbb42aac20','201608',7480),
('557886272424402ea34e7499a2af303a','201608',7484.4),
('2cf3959d527644acb1e0854c0a9ab099','201608',7629),
('3667290da9a641a2be668abdd82e6cd8','201608',4410.49),
('34702066e0904beb940c1eb3162e6521','201606',8000),
('3cee1bf6c4d441dd9fdb9a7764e5d683','201607',4661.55),
('3f48c92f05694e9ca6f6c3261309521f','201608',8200),
('8ecdc86c3633413b89a8aed4a3004d29','201608',8360),
('b46f73d5deeb4e9086d52edb1b1e1de4','201606',5000),
('c491703b1df94632ba2b956ca13c11a3','201608',9122),
('27ca2c86c7c94904a29c12eb3ba26a61','201607',3996.3),
('34702066e0904beb940c1eb3162e6521','201606',3500),
('8ac9fb0f4a6946e49618c5e0b0542e30','201608',10009.33),
('3e9321fef61b41d0878f7c511433c248','201607',7963),
('70949248effe44458782bedaf6e6ae33','201606',12245),
('2dcad62e0df54918a40c6050be1c4967','201607',10118),
('2ac0598fcc574ba5a529175e99ea9c84','201608',13538.24),
('27ca2c86c7c94904a29c12eb3ba26a61','201607',16292.89),
('946bfa4eabd946beb05962d22f752055','201607',23822)
]
add_three_month(('946bfa4eabd946beb05962d22f752055','201607',23822))