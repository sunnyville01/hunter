






# A buy order will be of 0.005 btc per coin at cbridge
# Check price at cryptopia where volumes sums to 0.01btc: bidPrice
# Place buy order 15% lower than bidPrice: buyPrice
#     Adjust buyPrice if bidPrice moves outside of 12% - 18% of it
# Play sound if a (buyOrder) gets filled at cbridge
# Check wallet statuses of all the (commonCoins)
# Can later add cbridge to bittrex, binances and other exchanges with common coins
#     Also Coinexchange and Idex to all the other exchanges as well

# # Possible Issues
# Pump and dump
#     Perhaps ignore coins that have gone up more than 30% in 24hours, and remove buyOrders for it
