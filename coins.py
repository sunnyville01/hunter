class Coins:

    # Ignore Coins
    binance_ignore = set(['USDC'])
    cbridge_ignore = set(['PCN', 'XGOX', 'XP'])

    # Coinex
    coinex_to_bittrex = set(['DGB', 'MOC', 'SALT', 'STORJ', 'ZEC', 'ZCL', 'SLR', 'GRS', 'SOLVE', 'CMCT', 'MTL', 'GNT', 'GTO', 'MUE', 'ZRX', 'LRC', 'BLK', 'XVG', 'PIVX', 'SRN', 'EGC', 'BAT', 'SNT', 'POWR', 'KMD', 'FTC', 'ETC', 'BOXX', 'DNT', 'RVN', 'OCN', 'ENJ', 'SYNX', 'MANA', 'BSD', 'POT', 'MONA', 'OMG', 'PAY', 'EMC', 'CVC', 'BCPT', 'NLC2', 'PAX', 'RVR', 'LOOM', 'MEME'])
    coinex_to_binance = set(['MITH', 'KNC', 'MTH', 'GVT', 'USDC', 'REQ', 'BRD', 'PPT', 'BNB', 'FUEL'])
    coinex_to_binance = coinex_to_binance - binance_ignore
    coinex_to_hitbtc = set(['ABYSS', 'AXPR', 'BTX', 'DGTX', 'ERT', 'FACE', 'JBC',  'PIX', 'PKT', 'PRE', 'PXG', 'R', 'REX', 'SCL', 'STX', 'SWM', 'TAAS'])
    coinex_to_cbridge = set(['FGC', 'DEV', 'UFO', 'GTM', 'LGS', 'BND', 'EQT', 'BTXC', 'IFX', 'PCN', 'PHON', 'BLCR', 'DMB', 'EXT', 'XGOX', 'XP', 'GBX', 'CATO', 'SINS', 'OLMP', 'P2P', 'BIR', 'VSX', 'XSH', 'GIN', 'SMART', 'GRPH', 'PAWS', 'ECC', 'OPC', 'BITG', 'ARION', 'APR', 'FLM', 'LRM', 'MONK', 'DSR', 'FLASH', 'AEG', 'XMCC', 'VIPS', 'AGM', 'NRG', 'XAP', 'GFR', 'FLN', 'LPC', 'ACED', 'UNIFY', 'PHR', 'SUQA', 'BTDX', 'PRJ', 'XLR', 'VITAE', 'IC', 'C2P', 'RUP', 'TRTT', 'BTCHP', 'CRAVE', 'ECA', '1X2'])
    coinex_to_cbridge = coinex_to_cbridge - cbridge_ignore

    # Cbridge
    cbridge_to_bittrex = set(['BAT', 'BAY', 'BLOCK', 'CLOAK', 'CRW', 'DASH', 'DGB', 'DMD', 'DYN', 'ENJ', 'ETH', 'EXCL', 'GRS', 'LTC', 'MONA', 'MUE', 'NPXS', 'OMG', 'PINK', 'PIVX', 'POWR', 'QTUM', 'RVN', 'RVR', 'SEQ', 'SLS', 'SYNX', 'VRC', 'VRM', 'VTC', 'XMR', 'XRP', 'XVG', 'XZC', 'ZEC'])
    cbridge_to_bittrex = cbridge_to_bittrex - cbridge_ignore


# BITTREX PMA RDD REP XZC
# BINANCE BCHABC HOT NPXS
# hitbtc DCN
# CBRIDGE GRPH
