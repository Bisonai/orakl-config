# Orakl Config

## Adapter

| name                                                                                 | adapterHash                                                        | decimals | feeds |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ | -------- | ----- |
| [ADA-USDT](https://bisonai.github.io/orakl-config/adapter/ada-usdt.adapter.json)     | 0x0cb4cf2bbe73c14b1ac4efdbb7f9fe6d96c53f722946eb624d0f11076f5b0ed6 | 8        | 10    |
| [BNB-USDT](https://bisonai.github.io/orakl-config/adapter/bnb-usdt.adapter.json)     | 0x8b4d886ffb1b1f24bd6069f648b03413d79ffcf84f56f3ae23857a02fa4186a5 | 8        | 8     |
| [BTC-USD](https://bisonai.github.io/orakl-config/adapter/btc-usd.adapter.json)       | 0xfb03ebf457def32f2d28944ec58af6796ec87e0aad6e01760bc7037d6ac71ea3 | 8        | 5     |
| [BTC-USDT](https://bisonai.github.io/orakl-config/adapter/btc-usdt.adapter.json)     | 0xb0c3c252c76334d29db18a5324e9ee815d95395689b532e9e58c1ecc05411993 | 8        | 10    |
| [BUSD-USDT](https://bisonai.github.io/orakl-config/adapter/busd-usdt.adapter.json)   | 0x6e1a8237ab158c7a69a78f82f59033964c5d511b8ea9b42064d206f01868e081 | 8        | 7     |
| [DAI-USDT](https://bisonai.github.io/orakl-config/adapter/dai-usdt.adapter.json)     | 0x6409fc5c79c8943dc487417798af3342ed2a40846e53e6a957ec7f5737d72c95 | 8        | 7     |
| [DOGE-USDT](https://bisonai.github.io/orakl-config/adapter/doge-usdt.adapter.json)   | 0xc648c89b2677c019dda482bbcfd60a5d58be0a3f02df9503b182fcaefbe5fa15 | 8        | 10    |
| [DOT-USDT](https://bisonai.github.io/orakl-config/adapter/dot-usdt.adapter.json)     | 0x432cf9560d26116f8900891242ab36f957608862eaa6005d2935aa43ea4cd79a | 8        | 10    |
| [ETH-USD](https://bisonai.github.io/orakl-config/adapter/eth-usd.adapter.json)       | 0x0b754850b753b9eca61724dc780c02d5f9a62a08c8853b80a213a03d85e35729 | 8        | 5     |
| [ETH-USDT](https://bisonai.github.io/orakl-config/adapter/eth-usdt.adapter.json)     | 0x41fd9f73cb9b3a62225cf4ea8612b10cdbe4fcaedfc43e81854a4bf4815864c9 | 8        | 10    |
| [KLAY-USD](https://bisonai.github.io/orakl-config/adapter/klay-usd.adapter.json)     | 0x69f797b7591e939b45f8aa51766bd696dfc2707d6316743b3c8c8bdfac73eb93 | 8        | 2     |
| [KLAY-USDT](https://bisonai.github.io/orakl-config/adapter/klay-usdt.adapter.json)   | 0x83e72a0fdd9c43e21c1720ff0c10b0f76fe17426a96b5622bc59b92e58099d34 | 8        | 10    |
| [MATIC-USDT](https://bisonai.github.io/orakl-config/adapter/matic-usdt.adapter.json) | 0xaac691986b90ba59358d2b8bff58036bcfea21cbd9f82ab08915902bdb00cdb1 | 8        | 10    |
| [SHIB-USDT](https://bisonai.github.io/orakl-config/adapter/shib-usdt.adapter.json)   | 0x8300f3385e5843e0da2504964067ab0d81de054550826e60577602e50cffe48c | 8        | 8     |
| [SOL-USDT](https://bisonai.github.io/orakl-config/adapter/sol-usdt.adapter.json)     | 0xf8ba3eafdf66c135dcd093dbb1bfdb10dca956ee3c75b510f76407353eb251d0 | 8        | 10    |
| [TRX-USDT](https://bisonai.github.io/orakl-config/adapter/trx-usdt.adapter.json)     | 0xf7385af79a7201e79185c79ff80dfa9d39960bb5c0d62e837477e0f0a87df716 | 8        | 8     |
| [USDC-USDT](https://bisonai.github.io/orakl-config/adapter/usdc-usdt.adapter.json)   | 0x04c991c1f0504684d1d4f4bd689066c08f9b32bea47746510590489e810eb23d | 8        | 8     |
| [XRP-USDT](https://bisonai.github.io/orakl-config/adapter/xrp-usdt.adapter.json)     | 0x61dc4a3225212016c0cbe5deffa1db31e01837fb0a061ff1cf355650287e0162 | 8        | 10    |

## Aggregator Baobab

| name                                                                                         | aggregatorHash | address | heartbeat | threshold | absoluteThreshold | adapterHash                                                        |
| -------------------------------------------------------------------------------------------- | -------------- | ------- | --------- | --------- | ----------------- | ------------------------------------------------------------------ |
| [ETH-USD](https://bisonai.github.io/orakl-config/aggregator/default/eth-usd.aggregator.json) | -              | -       | 15000     | 0.05      | 0.1               | 0x0b754850b753b9eca61724dc780c02d5f9a62a08c8853b80a213a03d85e35729 |

## Aggregator Default

| name                                                                                               | aggregatorHash | address | heartbeat | threshold | absoluteThreshold | adapterHash                                                        |
| -------------------------------------------------------------------------------------------------- | -------------- | ------- | --------- | --------- | ----------------- | ------------------------------------------------------------------ |
| [ADA-USDT](https://bisonai.github.io/orakl-config/aggregator/default/ada-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x0cb4cf2bbe73c14b1ac4efdbb7f9fe6d96c53f722946eb624d0f11076f5b0ed6 |
| [BNB-USDT](https://bisonai.github.io/orakl-config/aggregator/default/bnb-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x8b4d886ffb1b1f24bd6069f648b03413d79ffcf84f56f3ae23857a02fa4186a5 |
| [BTC-USD](https://bisonai.github.io/orakl-config/aggregator/default/btc-usd.aggregator.json)       | -              | -       | 15000     | 0.05      | 0.1               | 0xfb03ebf457def32f2d28944ec58af6796ec87e0aad6e01760bc7037d6ac71ea3 |
| [BTC-USDT](https://bisonai.github.io/orakl-config/aggregator/default/btc-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0xb0c3c252c76334d29db18a5324e9ee815d95395689b532e9e58c1ecc05411993 |
| [BUSD-USDT](https://bisonai.github.io/orakl-config/aggregator/default/busd-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x6e1a8237ab158c7a69a78f82f59033964c5d511b8ea9b42064d206f01868e081 |
| [DAI-USDT](https://bisonai.github.io/orakl-config/aggregator/default/dai-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x6409fc5c79c8943dc487417798af3342ed2a40846e53e6a957ec7f5737d72c95 |
| [DOGE-USDT](https://bisonai.github.io/orakl-config/aggregator/default/doge-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0xc648c89b2677c019dda482bbcfd60a5d58be0a3f02df9503b182fcaefbe5fa15 |
| [DOT-USDT](https://bisonai.github.io/orakl-config/aggregator/default/dot-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x432cf9560d26116f8900891242ab36f957608862eaa6005d2935aa43ea4cd79a |
| [ETH-USD](https://bisonai.github.io/orakl-config/aggregator/default/eth-usd.aggregator.json)       | -              | -       | 15000     | 0.05      | 0.1               | 0x0b754850b753b9eca61724dc780c02d5f9a62a08c8853b80a213a03d85e35729 |
| [ETH-USDT](https://bisonai.github.io/orakl-config/aggregator/default/eth-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x41fd9f73cb9b3a62225cf4ea8612b10cdbe4fcaedfc43e81854a4bf4815864c9 |
| [KLAY-USD](https://bisonai.github.io/orakl-config/aggregator/default/klay-usd.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x69f797b7591e939b45f8aa51766bd696dfc2707d6316743b3c8c8bdfac73eb93 |
| [KLAY-USDT](https://bisonai.github.io/orakl-config/aggregator/default/klay-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x83e72a0fdd9c43e21c1720ff0c10b0f76fe17426a96b5622bc59b92e58099d34 |
| [MATIC-USDT](https://bisonai.github.io/orakl-config/aggregator/default/matic-usdt.aggregator.json) | -              | -       | 15000     | 0.05      | 0.1               | 0xaac691986b90ba59358d2b8bff58036bcfea21cbd9f82ab08915902bdb00cdb1 |
| [SHIB-USDT](https://bisonai.github.io/orakl-config/aggregator/default/shib-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x8300f3385e5843e0da2504964067ab0d81de054550826e60577602e50cffe48c |
| [SOL-USDT](https://bisonai.github.io/orakl-config/aggregator/default/sol-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0xf8ba3eafdf66c135dcd093dbb1bfdb10dca956ee3c75b510f76407353eb251d0 |
| [TRX-USDT](https://bisonai.github.io/orakl-config/aggregator/default/trx-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0xf7385af79a7201e79185c79ff80dfa9d39960bb5c0d62e837477e0f0a87df716 |
| [USDC-USDT](https://bisonai.github.io/orakl-config/aggregator/default/usdc-usdt.aggregator.json)   | -              | -       | 15000     | 0.05      | 0.1               | 0x04c991c1f0504684d1d4f4bd689066c08f9b32bea47746510590489e810eb23d |
| [XRP-USDT](https://bisonai.github.io/orakl-config/aggregator/default/xrp-usdt.aggregator.json)     | -              | -       | 15000     | 0.05      | 0.1               | 0x61dc4a3225212016c0cbe5deffa1db31e01837fb0a061ff1cf355650287e0162 |
