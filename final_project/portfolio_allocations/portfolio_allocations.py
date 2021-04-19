import pandas as pd

columns = ['ST', 'CB', 'PB', 'GO', 'CA']
df_alloc = pd.DataFrame([], columns=columns)

for i in range(100, -5, -5):
    for j in range(100-i, -5, -5):
        for k in range(100-i-j, -5, -5):
            for l in range(100-i-j-k, -5, -5):
                for m in range(100-i-j-k-l, -5, -5):
                    if i+j+k+l+m == 100:
                        df_alloc=df_alloc.append({'ST':i/100, 'CB':j/100, 'PB':k/100, 'GO':l/100, 'CA':m/100}, ignore_index=True)

df_alloc.to_csv(r"YOUR_PATH\portfolio_allocations.csv") #your_path should be replaced by the path of the folder

