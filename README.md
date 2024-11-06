Materials for EDC2024 messaging systems talk.

To run the examples:

`pip install .`

# pubsub

```
cd src/foodtruck/pubsub
python chef.py
python worker_id.py 1
python worker_id.py 2
python worker_id.py 3
python worker_id.py 4
python customer.py
```

# router-dealer

```
cd src/foodtruck/router
python router.py
python worker_id.py 1
python worker_id.py 2
python worker_id.py 3
python worker_id.py 4
python customer.py
```

# push-pull

```
cd src/foodtruck/pushpull
python worker_id.py 1
python worker_id.py 2
python worker_id.py 3
python worker_id.py 4
python customer.py
```

# request-reply

```
cd src/foodtruck/reqrep
python foodtruck.py
python customer.py
```
