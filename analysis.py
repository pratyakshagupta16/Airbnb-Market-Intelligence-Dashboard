import pandas as pd

df = pd.read_csv("Airbnb_Open_Data.csv")

df = df.drop(columns=["license","house_rules","last review"])

df["price"] = df["price"].replace(r"[\$,]", "", regex=True).astype(float)


print(df["price"].head())
print(df["price"].dtype)
print(df["price"].describe())

print(df["room type"].value_counts())

import matplotlib.pyplot as plt

room_counts = df["room type"].value_counts()

plt.bar(room_counts.index, room_counts.values)
plt.title("Airbnb Listings by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Number of Listings")
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
sns.histplot(df["price"], bins=50)

plt.title("Distribution of Airbnb Prices")
plt.xlabel("Price")
plt.ylabel("Number of Listings")

plt.show()


plt.figure(figsize=(8,5))
sns.boxplot(x="room type", y="price", data=df)

plt.title("Price Distribution by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Price")

plt.show()


top_locations = df["neighbourhood group"].value_counts().head(10)

plt.figure(figsize=(8,5))
top_locations.plot(kind="bar")

plt.title("Top 10 Neighbourhood Groups by Listings")
plt.xlabel("Neighbourhood Group")
plt.ylabel("Number of Listings")

plt.show()


avg_price = df.groupby("room type")["price"].mean()

plt.figure(figsize=(8,5))
avg_price.plot(kind="bar")

plt.title("Average Price by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Average Price")

plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(x=df["number of reviews"], y=df["price"])

plt.title("Price vs Number of Reviews")
plt.xlabel("Number of Reviews")
plt.ylabel("Price")

plt.show()


top_hosts = df["host name"].value_counts().head(10)

plt.figure(figsize=(8,5))
top_hosts.plot(kind="bar")

plt.title("Top 10 Hosts by Number of Listings")
plt.xlabel("Host Name")
plt.ylabel("Number of Listings")

plt.show()


avg_availability = df.groupby("room type")["availability 365"].mean()

plt.figure(figsize=(8,5))
avg_availability.plot(kind="bar")

plt.title("Average Availability by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Average Days Available")

plt.show()

top_reviews = df.sort_values(by="number of reviews", ascending=False).head(10)

print(top_reviews[["NAME", "price", "number of reviews"]])

country_counts = df["country"].value_counts().head(10)

plt.figure(figsize=(8,5))
country_counts.plot(kind="bar")

plt.title("Top Countries by Airbnb Listings")
plt.xlabel("Country")
plt.ylabel("Number of Listings")

plt.show()
