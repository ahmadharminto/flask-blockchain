### Konsep dasar / simulasi blockchain menggunakan Flask ###

Dalam 1 block, terdapat komponen :
* previous hash block
* index (nomor block)
* nonce
* transaksi
* timestamp

Beberapa API endpoint yang ada :
* `/blockchain` [GET]
* `/mine` [GET]
* `/new-transaction` [POST]
* `/add-node` [POST]
* `/node-sync` [GET]

