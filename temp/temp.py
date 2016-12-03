from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common import DbUtil


def get_db_session(ip):
    db_url = "mysql+pymysql://root:Aa123456@{ip}:3306/sibu_directsale"
    # 初始化数据库连接:
    engine = create_engine(db_url.format(ip=ip), connect_args={'charset': 'utf8'}, echo=True)
    # 创建DBSession类型:
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def repair_profit_total(list):
    for d in list:
        session = get_db_session(ip=DbUtil.get_db_ip(00))
        try:
            session.execute(
                "UPDATE sibu_directsale_profit_00.member_profit_total t SET t.deal_sum_money=%d WHERE t.member_id = '%s'" % (
                d[1], d[0]))
            session.commit()
        except:
            session.rollback()


list =  [('01ca49724b924dc385caa194e7bccc20', 5950),
        ('05d4338a4d69473fbbf6f666ee3a3860', 46240),
        ('0ccf6b6cf2a8454c81f724d163e99910', 15000),
        ('148a6c6e044c4f899768c6dac6250be0', 26700),
        ('1698b4e984d74efd82e94b72044f9300', 88600),
        ('1d286fecccf44955b2b3089fc698f4e0', 11800),
        ('22da94119a20494aa90454d8ac06ca90', 10000),
        ('286fb2de0a644e129a75e004051d8ce0', 11310),
        ('300b9813a4ea490c9720057d492e9350', 59175),
        ('31e58d3a792b4a7cb71e4dcd5f4ca510', 200000),
        ('34904c46f372438eaf1274f2cc63ff40', 60000),
        ('383eea92c62c499da9277251bf5e9f30', 75180),
        ('38876489a94c4d5f9f12ecb98ef7ad30', 23410),
        ('38f9acbd28404aa58bca521dd753add0', 1990),
        ('3a3cdf04bf4e4cf78ed54373d21a7880', 1990),
        ('3a75292935fd4177b8552fe63de9e130', 4900),
        ('3a844dbd3b8540cc9900685d1f713a20', 1990),
        ('4b2c594c24f54bf9ac661ebfbd36b710', 82000),
        ('4db0167a990d4a389ed24a17e46f5c20', 17700),
        ('55dbf5adc88e45959fd3f7c6c5ad6590', 20895),
        ('5734f0180dec4c488bae2797c5197c80', 10000),
        ('5e832baa9ecc45e6bfdfeb58d25b1040', 13400),
        ('61680d5ae8dc41988d35d5bd3f4f09a0', 4950),
        ('65afb494fe3948f995c931bb861e2160', 7880),
        ('65e9003b212c49aab7de2a6d7e608060', 22675),
        ('6df9a509e22b4ed8a4f5fde08175f620', 56600),
        ('6ff2e7e177454f7dbd516c7c78834c00', 14820),
        ('71b39a9c17bc4fb6ac8d9102e9889800', 1900),
        ('78e91b311b29442689ecc60695ab3780', 20300),
        ('7b8da46afe484409a6b220346aea0530', 48000),
        ('819763c754f94835bda31f55824ff4e0', 36700),
        ('85761c28bdc84d1da8c9dc010a55d490', 5900),
        ('867818241acd4096b7c233c2b3b35e40', 3980),
        ('8706dfba24c849f79a3e5a87f757ded0', 229600),
        ('87ea644771b948bd8790f300d568a9f0', 1990),
        ('885e5adb8ce747deae272d889a6e1920', 10580),
        ('8ad1d9309fdb43459fb99433a07285c0', 377500),
        ('8d6625d0d64b46acae4cb099b11363b0', 4950),
        ('8fd20ffb01f24914b2c8cc2fe4c53cd0', 336700),
        ('9124cbc9b54e4c0493ffe6c6f97d8fe0', 9950),
        ('9134a46e2e5c433ea38179ceb2a162c0', 5900),
        ('9d70a67d6814476a829e1be04802eac0', 14270),
        ('9dd07f92dc6a47c394cfd35861b14d70', 9880),
        ('9de253cacc63443ea0f2f4ba93088df0', 78400),
        ('9eaa253cd3d847f090c7b598001beb30', 99601),
        ('a08cf29473b549b1a3eb9a36cd93fd80', 18800),
        ('a28ebd3d182b4c738243ac8fd4af6810', 1990),
        ('a29f9905ade9440fa152f7d97fb3be20', 13815),
        ('a38d3dc8fb5d4874a2ff32ad3da99d30', 226000),
        ('a6a939a414da4ac6b9e394f2fd6250c0', 1990),
        ('a6ed7bf1954a4457a5d883dc149337c0', 12830),
        ('a881c12ebe324c408ac5e862d361a610', 7960),
        ('a881f057728a4c288a95878defd83370', 6900),
        ('ae79a8be81d3481e8622580505ad94e0', 40970),
        ('ae8e130c97ac411cbc9573065370ceb0', 9900),
        ('ae92cf417612486c8fbbc7d8043bf590', 37005),
        ('af592d951f7048b5ab00dee397badf10', 3980),
        ('b3f443db14334538bc50ea1b712e2e30', 19800),
        ('b4176dff7fe5453ca323470bd15bef30', 160915),
        ('b6700b16724a490ba0d7cc90041d12c0', 40000),
        ('b9d90dd937c14d80ae60748c4a4a3ee0', 116400),
        ('bb71049f27be46989a3e260fcaee55b0', 18750),
        ('bb8ef2ef1b3d4b34b0d671654a707740', 245000),
        ('c1e82b73b92a4ef4828ba30dc3231200', 7890),
        ('c713cec1d49049049a0a5354c2dd3f40', 7890),
        ('cb16f445a65a4679a2a221d2f3e49a50', 23865),
        ('cc9ba0046ba14bf391c0049444ce36a0', 300000),
        ('ccd78d90dbf748fdac191d2f21fd1970', 9950),
        ('cebeaf8dbf7b4d2489530022ae1fac80', 37600),
        ('d1000fc683354e99866ea83d1ece83c0', 5900),
        ('d4c09003d5e04b7e8b9f5f5a5f7aaef0', 150000),
        ('d58dc533ae3e42598c36d668c29e4b80', 22815),
        ('d8ac4abef01044ba9f08a22376cd9530', 65965),
        ('d9871ac02ceb46a79746d3b86a4dd440', 253000),
        ('dcc68674bc914c8cbcab41eea1dc8d00', 10200),
        ('e169e2c915a841168272295d6640ca70', 8800),
        ('e2a4c5b8c24b475c938e6e681f3d91f0', 5900),
        ('e50c87c2f7434939bb3ea5f6b9dd87a0', 100000),
        ('e82b6e684b0c451f92c74c992b6ec5e0', 3980),
        ('e93deca1a1a245b28c973b60b9306040', 98120),
        ('eb8c52c877eb478c8ad48d2377b67fc0', 58485),
        ('ec6edbc2c84d43a194cbfc2984549d50', 34765),
        ('eff74051f253485b8c5e8cba44b34360', 92169),
        ('f1c229715b0a49d390887a88b4d8c740', 4950),
        ('f55c920d30544372b017b4fc39048650', 459000),
        ('f97099ae261f482ca2725b071cdec3d0', 13870),
        ('fbc8788a41c1466ab6d6ef943b5ba910', 18820),
        ('fee4bc2d1f4d439dbc69b18c608ec9a0', 5900)]
