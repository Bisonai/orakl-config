## Adapter

| name                                          | adapterHash                                                        | decimals | feeds |
| --------------------------------------------- | ------------------------------------------------------------------ | -------- | ----- |
| [ADA-USDT](adapter/ada-usdt.adapter.json)     | 0x3687675a0761d814147ac24366bb558b991397e5cabc6ed31498ba11b6125489 | 8        | 9     |
| [BNB-USDT](adapter/bnb-usdt.adapter.json)     | 0x8b4d886ffb1b1f24bd6069f648b03413d79ffcf84f56f3ae23857a02fa4186a5 | 8        | 8     |
| [BTC-USD](adapter/btc-usd.adapter.json)       | 0xfb03ebf457def32f2d28944ec58af6796ec87e0aad6e01760bc7037d6ac71ea3 | 8        | 5     |
| [BTC-USDT](adapter/btc-usdt.adapter.json)     | 0x428f92e44e58b056bf93283c185a2a9c493a020f3692ba6d79112e79e3178490 | 8        | 9     |
| [BUSD-USDT](adapter/busd-usdt.adapter.json)   | 0xcdd026d2200555d3c7e7317df0fde759e2688d165fced268f8e9469f3c195bbf | 8        | 6     |
| [DAI-USDT](adapter/dai-usdt.adapter.json)     | 0x0e0c7b9f61f34aa68cd9fcd48e6fef8ebca763171626b808671c9e2d79cf100d | 8        | 6     |
| [DOGE-USDT](adapter/doge-usdt.adapter.json)   | 0x4ec5aa686e27c152457bfe8256741316eebb100cb62eb8a1a93590e058b045a0 | 8        | 9     |
| [DOT-USDT](adapter/dot-usdt.adapter.json)     | 0x9c7a66a871649601bdccbd3a477e1f62f22856a745b86fa14ffde22e3a72151b | 8        | 8     |
| [ETH-USD](adapter/eth-usd.adapter.json)       | 0x0b754850b753b9eca61724dc780c02d5f9a62a08c8853b80a213a03d85e35729 | 8        | 5     |
| [ETH-USDT](adapter/eth-usdt.adapter.json)     | 0x65c601a931e65d7708d7e69e25615eeec2fcc6c7a1b5de095370efc2948edaa1 | 8        | 9     |
| [KLAY-USD](adapter/klay-usd.adapter.json)     | 0x69f797b7591e939b45f8aa51766bd696dfc2707d6316743b3c8c8bdfac73eb93 | 8        | 2     |
| [KLAY-USDT](adapter/klay-usdt.adapter.json)   | 0x28685856d05c545536c1fe0211c2d3b042a4e4346c8ae071f32893873da29c3d | 8        | 9     |
| [MATIC-USDT](adapter/matic-usdt.adapter.json) | 0x0ec26a8d32d68ba70c528e2adc204b546f9a103eb006ce2d421079be9990e449 | 8        | 9     |
| [SHIB-USDT](adapter/shib-usdt.adapter.json)   | 0x8300f3385e5843e0da2504964067ab0d81de054550826e60577602e50cffe48c | 8        | 8     |
| [SOL-USDT](adapter/sol-usdt.adapter.json)     | 0x6de578980052d37436cdbc5b478691bb5b8237302d058fa3f69b1d3a7639bfe2 | 8        | 9     |
| [TRX-USDT](adapter/trx-usdt.adapter.json)     | 0xa18dbcc041ad0373929711bc3570e7da99659a370db1665699092a5b231dd8fe | 8        | 7     |
| [USDC-USDT](adapter/usdc-usdt.adapter.json)   | 0xcc5560356e56fd70153a9e928967b363189360167d55e9844d69e357b32ed6ca | 8        | 7     |
| [XRP-USDT](adapter/xrp-usdt.adapter.json)     | 0x8fc3bf663dcfd380be2e9941dcc163cff1f14ef1d4b7f4140ed2fce34961c4cd | 8        | 9     |

## Aggregator Baobab

| name                                                       | aggregatorHash                                                     | address                                    | heartbeat | threshold | absoluteThreshold | adapterHash                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------ | --------- | --------- | ----------------- | ------------------------------------------------------------------ |
| [BNB-USDT](aggregator/baobab/bnb-usdt.aggregator.json)     | 0xbb42e0a9c45b898b29b763e28c2aaf3c117fb638fd8035378181b7cd6b613bd3 | 0x4fd37F2a8Ff009467F7EB390fc930B922519EfC0 | 15000     | 0.05      | 0.1               | 0x8b4d886ffb1b1f24bd6069f648b03413d79ffcf84f56f3ae23857a02fa4186a5 |
| [BTC-USDT](aggregator/baobab/btc-usdt.aggregator.json)     | 0xe9d72126d3d2017757f2c44ccaaec3ea541e043e0fb976f04ce900d857481d92 | 0x8e850a10709E3b87Ec9aBf5D689530ADb18fa87D | 15000     | 0.05      | 0.1               | 0x428f92e44e58b056bf93283c185a2a9c493a020f3692ba6d79112e79e3178490 |
| [BUSD-USDT](aggregator/baobab/busd-usdt.aggregator.json)   | 0x6594894b9be37ca796ea26e616a4934b9568aab41d17e90385404ba26e57a277 | 0x3EF5eB3b0356B61D562e847e96A524d81b33dbD3 | 15000     | 0.05      | 0.1               | 0xcdd026d2200555d3c7e7317df0fde759e2688d165fced268f8e9469f3c195bbf |
| [DAI-USDT](aggregator/baobab/dai-usdt.aggregator.json)     | 0xc5d9f1ed91a9bfe17b32f6495f96e4ea16c3605a4580c58ff90d27260d0bcc6d | 0x0B642034f2851192E040Ea1041810cB337aD321f | 15000     | 0.05      | 0.1               | 0x0e0c7b9f61f34aa68cd9fcd48e6fef8ebca763171626b808671c9e2d79cf100d |
| [DOT-USDT](aggregator/baobab/dot-usdt.aggregator.json)     | 0x59b1bc11d0eb079e7df154b3c8082c28f3fee9825c684ab131fd79ea24b58cf2 | 0x1a8a7E47A6A9981d3b420B96F70923f5da0d1074 | 15000     | 0.05      | 0.1               | 0x9c7a66a871649601bdccbd3a477e1f62f22856a745b86fa14ffde22e3a72151b |
| [ETH-USDT](aggregator/baobab/eth-usdt.aggregator.json)     | 0x9b930b9560a8ccd88a1024a60e4ae0830f092321d07bd1ca2e948cc8d6c7ab2b | 0xcAAF00e95ea71Bb7f190AFc0eafC4E3086773b25 | 15000     | 0.05      | 0.1               | 0x65c601a931e65d7708d7e69e25615eeec2fcc6c7a1b5de095370efc2948edaa1 |
| [KLAY-USDT](aggregator/baobab/klay-usdt.aggregator.json)   | 0x2d2f2602e26ac3de83ce7abbe9cc4fe99d971765b4328c4c659018e0356fea71 | 0x9DcD36A42Dabe856cD63a3011BBE6b51CC733CD6 | 15000     | 0.05      | 0.1               | 0x28685856d05c545536c1fe0211c2d3b042a4e4346c8ae071f32893873da29c3d |
| [MATIC-USDT](aggregator/baobab/matic-usdt.aggregator.json) | 0x980c2e3d135b6a25720716652d3f07f6225ec389fe54b8bbdd1a197263f6f681 | 0x38E0f7a626Efe241cCBe6EB2aA65273a9D6321Ce | 15000     | 0.05      | 0.1               | 0x0ec26a8d32d68ba70c528e2adc204b546f9a103eb006ce2d421079be9990e449 |
| [SOL-USDT](aggregator/baobab/sol-usdt.aggregator.json)     | 0xcdf65156d5d4adf7e8a79e81f0ace9bacd9edb5e1fd64a4e9de38739df2b13cb | 0xc9FA32b6DC26010c0811CCd43f6436C883C6E0ff | 15000     | 0.05      | 0.1               | 0x6de578980052d37436cdbc5b478691bb5b8237302d058fa3f69b1d3a7639bfe2 |
| [TRX-USDT](aggregator/baobab/trx-usdt.aggregator.json)     | 0x5c7e2bfe50cc780ede1769dd166a8e1840dca5c971bf4f3b659ff0eaa6eae7e6 | 0x70eF30152a6d37032831DcA7A78890584b4919f5 | 15000     | 0.05      | 0.1               | 0xa18dbcc041ad0373929711bc3570e7da99659a370db1665699092a5b231dd8fe |
| [USDC-USDT](aggregator/baobab/usdc-usdt.aggregator.json)   | 0xc5caa27efa50423d47116845154b27dc6fafa81056f623ad6797bb2965283cc3 | 0x96D808d3b82d07EBE9803D85b2EA9c68dAe831a8 | 15000     | 0.05      | 0.1               | 0xcc5560356e56fd70153a9e928967b363189360167d55e9844d69e357b32ed6ca |

## Aggregator Default

| name                                                        | aggregatorHash | address | heartbeat | threshold | absoluteThreshold | adapterHash                                                        |
| ----------------------------------------------------------- | -------------- | ------- | --------- | --------- | ----------------- | ------------------------------------------------------------------ |
| [ADA-USDT](aggregator/default/ada-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x3687675a0761d814147ac24366bb558b991397e5cabc6ed31498ba11b6125489 |
| [BNB-USDT](aggregator/default/bnb-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x8b4d886ffb1b1f24bd6069f648b03413d79ffcf84f56f3ae23857a02fa4186a5 |
| [BTC-USD](aggregator/default/btc-usd.aggregator.json)       | -              | -       | 15000     | 0.05      | 0.1               | 0xfb03ebf457def32f2d28944ec58af6796ec87e0aad6e01760bc7037d6ac71ea3 |
| [BTC-USDT](aggregator/default/btc-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x428f92e44e58b056bf93283c185a2a9c493a020f3692ba6d79112e79e3178490 |
| [BUSD-USDT](aggregator/default/busd-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0xcdd026d2200555d3c7e7317df0fde759e2688d165fced268f8e9469f3c195bbf |
| [DAI-USDT](aggregator/default/dai-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x0e0c7b9f61f34aa68cd9fcd48e6fef8ebca763171626b808671c9e2d79cf100d |
| [DOGE-USDT](aggregator/default/doge-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x4ec5aa686e27c152457bfe8256741316eebb100cb62eb8a1a93590e058b045a0 |
| [DOT-USDT](aggregator/default/dot-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x9c7a66a871649601bdccbd3a477e1f62f22856a745b86fa14ffde22e3a72151b |
| [ETH-USD](aggregator/default/eth-usd.aggregator.json)       | -              | -       | 15000     | 0.05      | 0.1               | 0x0b754850b753b9eca61724dc780c02d5f9a62a08c8853b80a213a03d85e35729 |
| [ETH-USDT](aggregator/default/eth-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x65c601a931e65d7708d7e69e25615eeec2fcc6c7a1b5de095370efc2948edaa1 |
| [KLAY-USD](aggregator/default/klay-usd.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x69f797b7591e939b45f8aa51766bd696dfc2707d6316743b3c8c8bdfac73eb93 |
| [KLAY-USDT](aggregator/default/klay-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x28685856d05c545536c1fe0211c2d3b042a4e4346c8ae071f32893873da29c3d |
| [MATIC-USDT](aggregator/default/matic-usdt.aggregator.json) | -              | -       | 15000     | 0.05      | 0.1               | 0x0ec26a8d32d68ba70c528e2adc204b546f9a103eb006ce2d421079be9990e449 |
| [SHIB-USDT](aggregator/default/shib-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x8300f3385e5843e0da2504964067ab0d81de054550826e60577602e50cffe48c |
| [SOL-USDT](aggregator/default/sol-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x6de578980052d37436cdbc5b478691bb5b8237302d058fa3f69b1d3a7639bfe2 |
| [TRX-USDT](aggregator/default/trx-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0xa18dbcc041ad0373929711bc3570e7da99659a370db1665699092a5b231dd8fe |
| [USDC-USDT](aggregator/default/usdc-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0xcc5560356e56fd70153a9e928967b363189360167d55e9844d69e357b32ed6ca |
| [XRP-USDT](aggregator/default/xrp-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x8fc3bf663dcfd380be2e9941dcc163cff1f14ef1d4b7f4140ed2fce34961c4cd |
