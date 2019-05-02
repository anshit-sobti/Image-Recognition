data = [
  {
    "url": "https://m.media-amazon.com/images/I/71oYHZQJK9L._AC_UL436_.jpg",
    "asin": "B0776M8VY1"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/618oANL1phL._SX425_.jpg",
    "asin": "B079TGL2BZ"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/51NV2ntjBnL._SX679_.jpg",
    "asin": "B07MKTMD6T"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/51YXG1bDM5L._SY879_.jpg",
    "asin": "B07K97BQDF"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/81Jk5oP-DmL._SX679_.jpg",
    "asin": "B01MUTHPSQ"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/81vEQbj98jL._SX679_.jpg",
    "asin": "B0734HTKP1"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/715tYiaXBtL._SL1500_.jpg",
    "asin": "B006IY89ZA"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/71qKTfZlOIL._UX679_.jpg",
    "asin": "B01M9ER4N1"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/61dJdXjqZYL._UX679_.jpg",
    "asin": "B07M78RXW8"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/81VO3hTdtCL._UY879_.jpg",
    "asin": "B07MYDG28L"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/815RsX3K5dL._UY879_.jpg",
    "asin": "B07BKMWP6J"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/713aB0VgS1L._SL1500_.jpg",
    "asin": "B07CGW7KL9"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/61J7RgQQInL._SL1001_.jpg",
    "asin": "B07D7W6CP5"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/61HahnTbx7L._SL1204_.jpg",
    "asin": "B078HSVK7M"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/71qremuSA%2BL._UX679_.jpg",
    "asin": "B015SIKOPE"
  },
  {
    "url": "https://images-na.ssl-images-amazon.com/images/I/61GJPL1hCpL._SX679_.jpg",
    "asin": "B071WLXKB2"
  }
]


dic = {}

for d in data:
    dic[d['asin']] = d['url']

print dic
    