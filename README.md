### Commands
creates tables for apps without migrations
```
python manage.py migrate --run-syncdb 
```

### Production environment vairables
| key | description |
|-----------------|------------------------------|
| SECRET_KEY | django secret key|
| EMAIL | support email |
| EMAIL_PASSWORD | support smtp email password |
| POSTGRESS_DATABASE_URL| postgress database url |