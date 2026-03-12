import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/rfm_segments.csv')

df["Segment"].value_counts().plot(kind='bar', color='skyblue')
plt.tick_params(axis='x', rotation=45)
plt.xlabel('Segment')
plt.ylabel('Müşteri Sayısı')
plt.title('Segmentlere Göre Müşteri Dağılımı')
plt.tight_layout()
plt.show()

df.groupby("Segment")["Monetary"].mean().plot(kind="bar")
plt.title("Segmentlere Göre Ortalama Harcama")
plt.xlabel("Segment")
plt.ylabel("Ortalama Harcama (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

colors = {
    "Daimi M.": "green",
    "Sadik M.": "blue",
    "Yeni M.": "orange",
    "Riskli M.": "red",
    "Kayip M.": "gray"
}

for segment, group in df.groupby("Segment"):
    plt.scatter(group["Recency"], group["Monetary"], 
                c=colors[segment], label=segment, alpha=0.5)

plt.xlabel("Recency (Gün)")
plt.ylabel("Monetary (£)")
plt.title("Recency vs Monetary - Segment Dağılımı")
plt.legend()
plt.tight_layout()
plt.show()