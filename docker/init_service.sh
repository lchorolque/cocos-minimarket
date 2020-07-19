
#!/bin/bash
docker-compose exec backend bash -c "
    ./manage.py migrate
    ./manage.py load_products_n_categories
    ./manage.py load_stores
    ./manage.py load_stocks
    ./manage.py load_vouchers
    "

