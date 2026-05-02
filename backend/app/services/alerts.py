def evaluate_price_trend(first_price,last_price):
    if not first_price or not last_price:return None,0
    c=(last_price-first_price)/first_price*100
    if c>15:return 'red',c
    if c>7:return 'yellow',c
    if c<-5:return 'positive',c
    return None,c
