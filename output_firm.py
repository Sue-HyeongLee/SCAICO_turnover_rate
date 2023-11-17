# basic 
import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
import sys

# topic modeling
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
from gensim.models import KeyedVectors

import pickle

# ml
import joblib


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

def topic_modeling(df):
    model_adv = KeyedVectors.load("tp_model/tp_adv/tp_adv_model")
    model_dadv = KeyedVectors.load("tp_model/tp_dadv/tp_dadv_model")

    with open('input/corpus_adv.pkl', 'rb') as lf:
        corpus_adv = pickle.load(lf)
    with open('input/corpus_dadv.pkl', 'rb') as lf:
        corpus_dadv = pickle.load(lf)
    
    num_topics_adv = 6
    num_topics_dadv = 7

    output_df_adv = pd.DataFrame({'company_name':df.company_name})
    for col in range(num_topics_adv):
        tmp = str(col)
        output_df_adv[tmp] = float(0)
    output_df_adv.index = [i for i in range(len(output_df_adv))]

    output_df_dadv = pd.DataFrame({'company_name':df.company_name})
    for col in range(num_topics_dadv):
        tmp = str(col)
        output_df_dadv[tmp] = float(0)
    output_df_dadv.index = [i for i in range(len(output_df_dadv))]

    for i, dt in enumerate(model_adv.get_document_topics(corpus_adv)):
        for val in dt:

            idx = str(val[0])
            pt = val[1]

            output_df_adv.at[i,idx] = pt

    for i, dt in enumerate(model_dadv.get_document_topics(corpus_dadv)):
        for val in dt:

            idx = str(val[0])
            pt = val[1]

            output_df_dadv.at[i,idx] = pt
    # output_df

    df = df.drop(['adv','dadv'], axis = 1)

    # adv
    output_df_adv = output_df_adv.dropna()

    col_adv = list(output_df_adv.columns)

    for i in range(1, len(col_adv)):
        col_adv[i] = "adv_topic_"+col_adv[i]
    output_df_adv.columns = col_adv

    # dadv
    output_df_dadv = output_df_dadv.dropna()

    col_dadv = list(output_df_dadv.columns)

    for i in range(1, len(col_dadv)):
        col_dadv[i] = "dadv_topic_"+col_dadv[i]
    output_df_dadv.columns = col_dadv

    output_df = pd.merge(output_df_adv, output_df_dadv ,how='inner')
    output_df = pd.merge(output_df, df ,how='inner')

    for feature in list(output_df.columns)[1:-1]:
        if feature != 'dadv_topic_4':
            nonzero_indices = output_df[feature] != 0  # 0이 아닌 값의 인덱스를 찾음
            output_df[feature] = np.log1p(output_df[feature])
    output_df = output_df.rename(columns={"average_salary":"average_salary(만원)", "total_sale":"total_sale(억원)"})
    return output_df

def show_strength_no_data(output_df):

    threshold = 0.1
    passing_feature = ['company_name','turn_over_rate']
    for i in output_df:
        if (i not in passing_feature):
            f_data = output_df[i].to_list()[0]
            if f_data >= threshold:
                print(topic_dic[i],':',f_data)
                print('해당 특징은 전체 데이터 중에서 상위 {:.3f}% 입니다.'.format(percentileofscore(df[i],f_data)))

    return

def ml_prediction(output_df):
    lgbm_model = joblib.load('ml_model/tp_lgbm_reg_model.pkl')
    xgb_model = joblib.load('ml_model/tp_xgb_reg_model.pkl')

    y_target = output_df['turn_over_rate']
    x_data = output_df.drop(['company_name','turn_over_rate'], axis = 1, inplace = False)

    print("LGBM 모델로 예측된 이직률 :",lgbm_model.predict(x_data))
    print("XGB 모델로 예측된 이직률 :",xgb_model.predict(x_data))
    print("실제 해당 회사의 이직률 : ", y_target.to_list())
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

    output_file_name = 'output_firm.txt'

    sys.stdout = open(output_file_name, 'w')

    print('회사의 이름을 입력하세요 (종료를 원한다면 x) ::')
    
    usr_input = input()
    print(usr_input)
    print()
    if usr_input in df['company_name'].to_list():
        show_company_strength(df,usr_input,topic_dic)
    else:
        df = pd.read_csv("sample_input.csv")
        df = df.drop(["Unnamed: 0"], axis=1)
        output_df = topic_modeling(df)
        show_strength_no_data(output_df)
        print()
        ml_prediction

    sys.stdout.close()
    print(f"출력 로그가 '{output_file_name}' 파일에 저장되었습니다.")
