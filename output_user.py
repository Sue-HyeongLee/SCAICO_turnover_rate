import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
import sys

def show_max(df, topic, topic_dic):

    if topic not in df.columns.to_list():
        print('해당 토픽은 데이터베이스에 없습니다.')
        return
    
    # col = df.columns.to_list().index(type)
    df = df.sort_values(topic, ascending = False)
    tmp = df.head()
    print('{} 특징의 상위 5개의 기업은 다음과 같습니다.'.format(topic_dic[topic]))
    print()
    for i in tmp['company_name']:
        print(i)
    print()
    return

def show_company_strength(df,name,topic_dic):
    
    if name not in df['company_name'].to_list():
        print('해당 회사는 데이터베이스에 없습니다.')
        return
    
    print('프로그램에서 찾은',name,' 의 특징은 다음과 같습니다.')
    print()

    tmp = df[df['company_name'] == name]

    threshold = 0.1
    passing_feature = ['company_name','turn_over_rate']
    for i in tmp:
        if (i not in passing_feature):
            f_data = tmp[i].to_list()[0]
            if f_data >= threshold:
                print(topic_dic[i],':',f_data)
                print('해당 특징은 전체 데이터 중에서 상위 {:.3f}% 입니다.'.format(percentileofscore(df[i],f_data)))
                print()

    return 

if __name__ == '__main__':
    topic_dic = {'adv_topic_0': '잘 설립된 복지 시스템',
                'adv_topic_1': '회사 시설 및 제도',
                'adv_topic_2': '여가 지원',
                'adv_topic_3': '자율적 근무환경',
                'adv_topic_4': '만족스러운 급여',
                'adv_topic_5': '직원 친화적 분위기',
                'dadv_topic_0': '보수적인 문화 및 진급의 어려움',
                'dadv_topic_1': '정규직 전환의 어려움',
                'dadv_topic_2': '열약한 업무 프로세스와 조직구조',
                'dadv_topic_3': '근무지 불만',
                'dadv_topic_4': '불확실한 성장 전망',
                'dadv_topic_5': '고객 응대 + 성과에 대한 압박',
                'dadv_topic_6': '수당 + 회사 시설 및 제도의 열약함',
                'average_salary': '평균 연봉 (만원)',
                'total_sale': '연 매출 (억원)'
                }
    df = pd.read_csv("tp_df.csv")
    df['total_sale'] =  df['total_sale'].astype(float)
    df = df.drop(["Unnamed: 0"], axis=1)

    output_file_name = 'output_user.txt'

    sys.stdout = open(output_file_name, 'w')

    print('특징 별 상위 5개 기업: 1 \n특정 회사의 특징 백분위로 확인 : 2\n나가기: x')
    
    usr_input = input()
    while usr_input != 'x':
        if usr_input == '1':
            print('다음의 토픽 중에서 선택해주세요: adv_topic_0~5, dadv_topic_0~6')
            topic = input()
            show_max(df,topic, topic_dic)
        elif usr_input == '2':
            company = input()
            show_company_strength(df,company,topic_dic)
        else:
            pass
        usr_input = input()
        print('특징 별 상위 5개 기업: 1 \n특정 회사의 특징 백분위로 확인 : 2\n나가기: x')
    
    sys.stdout.close()
    print(f"출력 로그가 '{output_file_name}' 파일에 저장되었습니다.")

