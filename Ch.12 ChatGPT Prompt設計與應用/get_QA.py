import pandas as pd
def get_QAlist(path):
    df = pd.read_csv(path)
    Q, A = df['題目'].values, df['解答'].values
    
    QA_list = [f'Q:{q} A:{a}' for q, a in zip(Q, A)]
    
    return QA_list