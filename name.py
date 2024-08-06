#假身份生成器，请勿用于违法行为

import random
import pandas as pd
from datetime import datetime
import os

# 读取数据文件
def load_data():

    county_df = pd.read_csv('data/county.csv', usecols=['code', 'name'])
    universities_df = pd.read_csv('data/universities.csv', usecols=['name'])
    
    return county_df, universities_df

county_df, universities_df = load_data()
area_code = str(random.choice(county_df['code'].tolist()))

# 生成姓名
def gen_name():
    with open('data/last_name.txt', 'r', encoding='utf-8') as file:
        last_names = file.read().splitlines()
    with open('data/first_name.txt', 'r', encoding='utf-8') as file:
        first_names = file.read().splitlines()
    last_name = random.choice(last_names).strip() 
    first_name_length = random.randint(1, 2)
    first_name = ''.join(random.choices(first_names, k=first_name_length)).strip() 
    
    return last_name + first_name

# 生成随机生日
def gen_birthday():
    year = random.randint(1980, 2015)
    month = random.randint(1, 12)
    day = random.randint(1, 31)

    if month in [4, 6, 9, 11]:
        day = min(day, 30)
    elif month == 2:
        day = min(day, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28)
        
    return f"{year:04d}-{month:02d}-{day:02d}"

# 生成身份证号码
def gen_id_card(birthday, area_code, gender):
    county_code = area_code[:6]
    gender_digit = random.randint(0, 1) * 2 + (1 if gender == '男' else 0) 
    check_digit = random.randint(0, 9)
    
    return f"{county_code}{birthday.replace('-', '')}{gender_digit:03d}{check_digit}"

# 生成手机号
def gen_mobile():
    prefixes = [
        '134', '135', '136', '137', '138', '139', '150', '151', '152', '157', 
        '158', '159', '170', '178', '182', '183', '184', '187', '188', '130', 
        '131', '132', '145', '150', '151', '152', '157', '170', '176', '185', 
        '186', '133', '149', '153', '170', '177', '180', '181', '189'
    ]
    prefix = random.choice(prefixes)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    mobile = f"{prefix}{suffix}"
    
    return mobile

# 生成家庭地址
def get_full_address(area_code):
    provinces_df = pd.read_json('data/provinces.json')[['code', 'name']]
    cities_df = pd.read_json('data/city.json')[['code', 'name']]
    county_df = pd.read_json('data/county.json')[['code', 'name']]
    town_df = pd.read_json('data/town.json')[['code', 'name']]
    
    province_code = area_code[:2]
    province_name = next((name for code, name in zip(provinces_df['code'], provinces_df['name']) if str(code).startswith(province_code)), 'Unknown Province')
    city_code = area_code[:4]
    city_name = next((name for code, name in zip(cities_df['code'], cities_df['name']) if str(code).startswith(city_code)), 'Unknown City')
    county_code = area_code[:6]
    county_name = next((name for code, name in zip(county_df['code'], county_df['name']) if str(code).startswith(county_code)), 'Unknown County')
    street_name = random.choice([name for code, name in zip(town_df['code'], town_df['name']) if str(code).startswith(county_code)])
    section_number = f"{random.randint(1, 300):03d}号"
    
    return f"{province_name}{city_name}{county_name}{street_name}{section_number}"

# 生成个人信息
def gen_person_info():
    name = gen_name()
    birthday = gen_birthday()
    gender = '男' if int(area_code[-1]) % 2 == 1 else '女'
    age = datetime.now().year - int(birthday.split('-')[0])
    id_card = gen_id_card(birthday, area_code, gender)
    mobile = gen_mobile()
    postal_code = area_code[:6]
    address = get_full_address(area_code)
    university = random.choice(universities_df['name'].tolist())
    occupation = random.choice(['学生', '教师', '工程师', '医生', '商人'])
    height = random.randint(150, 190)  # 身高范围
    weight = random.randint(40, 100)    # 体重范围
    blood_type = random.choice(['A', 'B', 'AB', 'O'])

    nationality = random.choice([
        '汉族', '藏族', '维吾尔族', '苗族', '壮族', 
        '满族', '侗族', '瑶族', '朝鲜族', '回族', 
        '土家族', '畲族', '苗族', '黎族', '哈尼族', 
        '阿昌族', '藏族', '瑶族', '土族', '仡佬族', 
        '彝族', '回族', '其他'
    ])
    occupation = random.choice([
        '学生', '教师', '工程师', '医生', '商人',
        '护士', '律师', '程序员', '设计师', '科学家',
        '会计', '记者', '销售员', '项目经理', '市场专员',
        '艺术家', '音乐家', '厨师', '司机', '建筑师',
        '心理咨询师', '生物学家', '化学家', '物理学家', '数据分析师',
        '网络安全专家', '系统管理员', '翻译', '社工', '环境保护专家',
        '保险代理人', '房地产经纪人', '美容师', '健身教练', '电工',
        '机械师', '农民', '运营经理', '公关专员', '企业家',
        '作家', '摄影师', '视频编辑', '网页开发员', '软件测试员'
    ])

    return {
        '名字': name,     
        '民族': nationality,
        '性别': gender,   
        '年龄': age,
        '生日': birthday,
        '家庭地址': address,     
        '身份证号码': id_card,
        '电话号码': mobile,
        '邮政编码': postal_code,
        '毕业院校': university,
        '职业': occupation,
        '身高': f"{height}cm",
        '体重': f"{weight}kg",
        '血型': f"{blood_type}型",
    }

# 输出个人信息
person_info = gen_person_info()
print("个人资料：")
for key, value in person_info.items():
    print(f"{key}: {value}")
