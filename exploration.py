import pandas as pd

# RFM segmentasyon fonksiyonu
def rfm_segmentation(recency, frequency, monetary):

    if recency == 4 and frequency == 4:
        return "Daimi M."
    elif recency >= 3 and frequency >= 3:
        return "Sadik M."
    elif recency >= 3 and frequency <= 2:
        return "Yeni M."
    elif recency <= 2 and frequency >= 3:
        return "Riskli M."
    else:
        return "Kayip M."    
    

#Excel dosyasını csv formatına dönüştürme    
#df = pd.read_excel('data/Online Retail.xlsx', sheet_name='Online Retail')
#df.to_csv('data/deneme.csv', index=False)

#CSV dosyasını okuma
df = pd.read_csv('data/Online Retail.csv')

print(df.info(), "\n***\n", 
      df.describe(), "\n***\n", 
      df.isnull().sum(), "\n***\n",
      df.head(), "\n***\n", 
      df.tail()
      )

#Boş değerleri temizleme
df = df.dropna(subset=['CustomerID'])

#Olumsuz miktar ve fiyatları temizleme
filtered_df  = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

#Tarihi datetime formatına çevirme
filtered_df["InvoiceDate"] = pd.to_datetime(filtered_df["InvoiceDate"], 
                                     format="%Y-%m-%d %H:%M:%S")
#Toplam fiyat sütunu ekleme
filtered_df["TotalPrice"] = filtered_df["Quantity"] * filtered_df["UnitPrice"]

#Müşteri başına toplam harcama ve alışveriş sıklığını hesaplama
max_date = filtered_df["InvoiceDate"].max()
recency = max_date - filtered_df.groupby("CustomerID")["InvoiceDate"].max()
monetary = filtered_df.groupby("CustomerID")["TotalPrice"].sum()
frequency = filtered_df.groupby("CustomerID")["InvoiceNo"].nunique()

#RFM dataframe oluşturma
rfm_df = pd.DataFrame({"Recency": recency,
                       "Frequency": frequency,
                       "Monetary": monetary,
                       })

rfm_df["Recency"] = rfm_df["Recency"].dt.days

#RFM skorlarını hesaplama
rfm_df["RecencyScore"] = pd.qcut(rfm_df["Recency"], 
                            4, 
                            labels=[4, 3, 2, 1]
                            )
rfm_df["FrequencyScore"] = pd.qcut(rfm_df["Frequency"].rank(method='first'), 
                              4, 
                              labels=[1, 2, 3, 4]
                              )
rfm_df["MonetaryScore"] = pd.qcut(rfm_df["Monetary"], 
                             4, 
                             labels=[1, 2, 3, 4]
                             )
rfm_df["Score"] = rfm_df["RecencyScore"].astype(str) + rfm_df["FrequencyScore"].astype(str) + rfm_df["MonetaryScore"].astype(str)
#RFM segmentlerini olusturma
rfm_df["Segment"] = rfm_df[["RecencyScore", "FrequencyScore", "MonetaryScore"]].apply(lambda x: rfm_segmentation(*x), axis=1)
rfm_df.to_csv('data/rfm.csv', index=True)
print(filtered_df.head())